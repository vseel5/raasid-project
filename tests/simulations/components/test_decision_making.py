import pytest
from datetime import datetime
from api.simulations.components.decision_making import (
    DecisionInput,
    DecisionOutput,
    DecisionMaker,
    decision_maker
)

@pytest.fixture
def sample_pose_data():
    return {
        'hand_position_score': 0.8,
        'body_position_score': 0.6,
        'movement_score': 0.7
    }

@pytest.fixture
def sample_contact_data():
    return {
        'contact_probability': 0.9,
        'location_score': 0.8,
        'force_score': 0.7
    }

@pytest.fixture
def sample_context_data():
    return {
        'game_situation_score': 0.7,
        'player_intent_score': 0.6,
        'play_context_score': 0.8
    }

@pytest.fixture
def decision_input(sample_pose_data, sample_contact_data, sample_context_data):
    return DecisionInput(
        pose_data=sample_pose_data,
        ball_contact_data=sample_contact_data,
        event_context_data=sample_context_data,
        frame_number=1
    )

def test_decision_input_validation():
    """Test that DecisionInput validates data correctly"""
    with pytest.raises(ValueError):
        DecisionInput(
            pose_data={},
            ball_contact_data={},
            event_context_data={},
            frame_number=-1
        )

def test_decision_output_validation():
    """Test that DecisionOutput validates data correctly"""
    with pytest.raises(ValueError):
        DecisionOutput(
            certainty_score=150,  # Invalid score > 100
            var_review_status=True,
            decision_reason="Test",
            confidence_metrics={}
        )

def test_analyze_pose():
    """Test pose analysis functionality"""
    maker = DecisionMaker()
    pose_data = {
        'hand_position_score': 0.8,
        'body_position_score': 0.6,
        'movement_score': 0.7
    }
    score, reason = maker._analyze_pose(pose_data)
    assert 0 <= score <= 1
    assert reason in ["Natural position", "Unnatural position"]

def test_analyze_contact():
    """Test contact analysis functionality"""
    maker = DecisionMaker()
    contact_data = {
        'contact_probability': 0.9,
        'location_score': 0.8,
        'force_score': 0.7
    }
    score, reason = maker._analyze_contact(contact_data)
    assert 0 <= score <= 1
    assert reason in ["No significant contact", "Significant contact detected"]

def test_analyze_context():
    """Test context analysis functionality"""
    maker = DecisionMaker()
    context_data = {
        'game_situation_score': 0.7,
        'player_intent_score': 0.6,
        'play_context_score': 0.8
    }
    score, reason = maker._analyze_context(context_data)
    assert 0 <= score <= 1
    assert reason in ["Normal play", "Suspicious play"]

def test_make_decision(decision_input):
    """Test the complete decision making process"""
    result = decision_maker.make_decision(decision_input)
    
    assert isinstance(result, DecisionOutput)
    assert 0 <= result.certainty_score <= 100
    assert isinstance(result.var_review_status, bool)
    assert isinstance(result.decision_reason, str)
    assert isinstance(result.confidence_metrics, dict)
    
    # Check confidence metrics
    assert 'pose_confidence' in result.confidence_metrics
    assert 'contact_confidence' in result.confidence_metrics
    assert 'context_confidence' in result.confidence_metrics
    assert 'final_confidence' in result.confidence_metrics

def test_make_decision_error_handling():
    """Test error handling in decision making"""
    invalid_input = DecisionInput(
        pose_data={'invalid': 'data'},
        ball_contact_data={'invalid': 'data'},
        event_context_data={'invalid': 'data'},
        frame_number=1
    )
    
    result = decision_maker.make_decision(invalid_input)
    assert result.certainty_score == 0.0
    assert result.var_review_status is True
    assert "Error" in result.decision_reason

def test_decision_weights():
    """Test that decision weights are properly applied"""
    maker = DecisionMaker()
    
    # Test pose weights
    pose_data = {
        'hand_position_score': 1.0,
        'body_position_score': 0.0,
        'movement_score': 0.0
    }
    score, _ = maker._analyze_pose(pose_data)
    assert abs(score - 0.4) < 0.01  # hand_position weight is 0.4
    
    # Test contact weights
    contact_data = {
        'contact_probability': 1.0,
        'location_score': 0.0,
        'force_score': 0.0
    }
    score, _ = maker._analyze_contact(contact_data)
    assert abs(score - 0.5) < 0.01  # contact_probability weight is 0.5
    
    # Test context weights
    context_data = {
        'game_situation_score': 1.0,
        'player_intent_score': 0.0,
        'play_context_score': 0.0
    }
    score, _ = maker._analyze_context(context_data)
    assert abs(score - 0.4) < 0.01  # game_situation weight is 0.4

def test_var_review_threshold():
    """Test VAR review threshold functionality"""
    from api.config import settings
    
    # Test with high certainty
    high_certainty_input = DecisionInput(
        pose_data={'hand_position_score': 1.0, 'body_position_score': 1.0, 'movement_score': 1.0},
        ball_contact_data={'contact_probability': 1.0, 'location_score': 1.0, 'force_score': 1.0},
        event_context_data={'game_situation_score': 1.0, 'player_intent_score': 1.0, 'play_context_score': 1.0},
        frame_number=1
    )
    result = decision_maker.make_decision(high_certainty_input)
    assert result.var_review_status is False
    
    # Test with low certainty
    low_certainty_input = DecisionInput(
        pose_data={'hand_position_score': 0.5, 'body_position_score': 0.5, 'movement_score': 0.5},
        ball_contact_data={'contact_probability': 0.5, 'location_score': 0.5, 'force_score': 0.5},
        event_context_data={'game_situation_score': 0.5, 'player_intent_score': 0.5, 'play_context_score': 0.5},
        frame_number=1
    )
    result = decision_maker.make_decision(low_certainty_input)
    assert result.var_review_status is True 