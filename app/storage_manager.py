import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, Any, Optional
import sqlite3
import hashlib

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = Path(base_dir)
        self.upload_dir = self.base_dir / "uploads"
        self.processed_dir = self.base_dir / "processed"
        self.metadata_dir = self.base_dir / "metadata"
        self.db_path = self.base_dir / "videos.db"
        
        # Create necessary directories
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_db()
        
        logger.info(f"Storage manager initialized at {self.base_dir}")

    def _init_db(self):
        """Initialize SQLite database for video metadata."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Create videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                video_id TEXT PRIMARY KEY,
                original_filename TEXT,
                file_path TEXT,
                file_size INTEGER,
                upload_time TEXT,
                status TEXT,
                processing_start_time TEXT,
                processing_end_time TEXT,
                processing_result TEXT,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def store_video(self, video_id: str, file_path: str, original_filename: str) -> str:
        """Store uploaded video and return the stored path."""
        try:
            # Calculate file hash
            file_hash = self._calculate_file_hash(file_path)
            
            # Create storage path
            stored_path = self.upload_dir / f"{video_id}_{file_hash}{Path(file_path).suffix}"
            
            # Move file to storage
            shutil.move(file_path, stored_path)
            
            # Store metadata in database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO videos (
                    video_id, original_filename, file_path, file_size,
                    upload_time, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                video_id,
                original_filename,
                str(stored_path),
                os.path.getsize(stored_path),
                datetime.now().isoformat(),
                "uploaded"
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored video {video_id} at {stored_path}")
            return str(stored_path)
            
        except Exception as e:
            logger.error(f"Error storing video {video_id}: {str(e)}")
            raise

    def store_processing_result(self, video_id: str, result: Dict[str, Any]):
        """Store video processing results."""
        try:
            # Store result as JSON
            result_path = self.metadata_dir / f"{video_id}_result.json"
            with open(result_path, 'w') as f:
                json.dump(result, f)
            
            # Update database
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE videos
                SET status = ?,
                    processing_end_time = ?,
                    processing_result = ?
                WHERE video_id = ?
            ''', (
                "processed",
                datetime.now().isoformat(),
                str(result_path),
                video_id
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored processing results for video {video_id}")
            
        except Exception as e:
            logger.error(f"Error storing processing results for {video_id}: {str(e)}")
            raise

    def get_video_info(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video information from database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM videos WHERE video_id = ?', (video_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                video_info = dict(zip(columns, row))
                
                # Load processing result if available
                if video_info.get('processing_result'):
                    with open(video_info['processing_result'], 'r') as f:
                        video_info['processing_result'] = json.load(f)
                
                return video_info
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting video info for {video_id}: {str(e)}")
            return None
        finally:
            conn.close()

    def update_status(self, video_id: str, status: str, error: Optional[str] = None):
        """Update video processing status."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if status == "processing":
                cursor.execute('''
                    UPDATE videos
                    SET status = ?,
                        processing_start_time = ?,
                        error_message = ?
                    WHERE video_id = ?
                ''', (status, datetime.now().isoformat(), error, video_id))
            else:
                cursor.execute('''
                    UPDATE videos
                    SET status = ?,
                        error_message = ?
                    WHERE video_id = ?
                ''', (status, error, video_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated status for video {video_id} to {status}")
            
        except Exception as e:
            logger.error(f"Error updating status for {video_id}: {str(e)}")
            raise

    def cleanup(self, video_id: str):
        """Clean up video files and metadata."""
        try:
            # Get video info
            video_info = self.get_video_info(video_id)
            if not video_info:
                return
            
            # Remove files
            if video_info.get('file_path') and os.path.exists(video_info['file_path']):
                os.remove(video_info['file_path'])
            
            result_path = self.metadata_dir / f"{video_id}_result.json"
            if result_path.exists():
                result_path.unlink()
            
            logger.info(f"Cleaned up files for video {video_id}")
            
        except Exception as e:
            logger.error(f"Error cleaning up video {video_id}: {str(e)}")
            raise

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest() 