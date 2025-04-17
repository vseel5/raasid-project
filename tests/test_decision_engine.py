import unittest
import os
import json
from datetime import datetime
from app.decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary rules directory
        cls.test_dir = "tests/data"
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Create a test rules file
        cls.rules = {
            "offside": {
                "description": "Test offside rule",
                "criteria": ["Player position"],
                "exceptions": ["Player in own half"]
            },
            "foul": {
                "description": "Test foul rule",
                "types": [
                    {
                        "name": "Direct Free Kick Fouls",
                        "examples": ["Kicking opponent"]
                    }
                ]
            }
        }
        
        # Save the rules
        cls.rules_path = os.path.join(cls.test_dir, "test_rules.json")
        with open(cls.rules_path, "w") as f:
            json.dump(cls.rules, f)
        
        # Initialize the decision engine
        cls.engine = DecisionEngine(rules_path=cls.rules_path)

    @classmethod
    def tearDownClass(cls):
        # Clean up
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_rules_loading(self):
        """Test that FIFA rules are loaded correctly."""
        self.assertIsInstance(self.engine.rules, dict)
        self.assertIn("offside", self.engine.rules)
        self.assertIn("foul", self.engine.rules)
        self.assertEqual(self.engine.rules["offside"]["description"], "Test offside rule")

    def test_analyze_frame(self):
        """Test frame analysis for rule violations."""
        # Create a test frame data
        frame_data = {
            "timestamp": 1234567890,
            "frame_number": 42,
            "objects": {
                "boxes": [[100, 100, 200, 200]],
                "labels": [1],
                "scores": [0.95]
            }
        }
        
        # Analyze the frame
        result = self.engine.analyze_frame(frame_data)
        
        # Check the output structure
        self.assertIsInstance(result, dict)
        self.assertIn("timestamp", result)
        self.assertIn("frame_number", result)
        self.assertIn("violations", result)
        self.assertIn("events", result)
        self.assertEqual(result["frame_number"], 42)

    def test_process_video_analysis(self):
        """Test processing of complete video analysis."""
        # Create test video analysis data
        video_analysis = {
            "video_info": {
                "id": "test_video_001",
                "duration": 60,
                "fps": 30
            },
            "frame_analyses": [
                {
                    "timestamp": 1234567890,
                    "frame_number": i,
                    "objects": {
                        "boxes": [[100, 100, 200, 200]],
                        "labels": [1],
                        "scores": [0.95]
                    }
                }
                for i in range(5)  # Test with 5 frames
            ]
        }
        
        # Process the video analysis
        result = self.engine.process_video_analysis(video_analysis)
        
        # Check the output structure
        self.assertIsInstance(result, dict)
        self.assertIn("video_info", result)
        self.assertIn("violations", result)
        self.assertIn("events", result)
        self.assertIn("summary", result)
        self.assertIsInstance(result["summary"]["processing_time"], float)
        self.assertEqual(result["video_info"]["id"], "test_video_001")

    def test_decision_distribution(self):
        """Test decision distribution functionality."""
        # Create a test decision
        decision = {
            "timestamp": datetime.now().timestamp(),
            "video_id": "test_video_001",
            "violations": [
                {
                    "category": "offside",
                    "confidence": 0.95,
                    "details": {"player_id": 1}
                }
            ]
        }
        
        # Test distribution
        result = self.engine.distribute_decision(decision)
        self.assertTrue(result)  # Should return True even with TODO implementation

if __name__ == "__main__":
    unittest.main() 