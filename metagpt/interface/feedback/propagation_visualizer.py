#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4
@Author  : Gemini
@File    : propagation_visualizer.py
"""

from typing import Dict, List, Any, Optional, Callable
import uuid
import time

# Placeholder for actual agent environment/message bus
# from metagpt.environment import Environment

class PropagationVisualizer:
    """Tracks and visualizes the propagation of feedback through the agent system.

    This class monitors the status of feedback processing across different agents
    and provides data to the frontend for visualizing the flow and impact.
    """

    def __init__(self, environment=None):
        """Initializes the PropagationVisualizer.

        Args:
            environment: The agent execution environment or message bus to monitor.
        """
        self._feedback_status: Dict[str, Dict[str, Any]] = {} # feedback_id -> status info
        # Status info might include: {'state': 'processing', 'current_agent': 'coder', 'affected_components': ['comp1'], 'timestamp': ...}
        self._subscribers: Dict[str, List[Callable]] = {} # feedback_id -> list of frontend callbacks

        self._environment = environment # For listening to agent events

        print("PropagationVisualizer initialized.")
        # Potentially start listening to environment events here if it's asynchronous

    def track_new_feedback(self, feedback_id: Optional[str] = None, initial_context: Optional[Dict] = None) -> str:
        """Starts tracking a new feedback item.

        Args:
            feedback_id: An optional specific ID for the feedback.
            initial_context: Optional initial context about the feedback (e.g., source artifact/component).

        Returns:
            The unique ID assigned to this feedback tracking instance.
        """
        if feedback_id is None:
            feedback_id = str(uuid.uuid4())

        print(f"Tracking new feedback: {feedback_id}")
        self._feedback_status[feedback_id] = {
            'state': 'received',
            'current_agent': None,
            'affected_components': initial_context.get('components', []) if initial_context else [],
            'history': [{'state': 'received', 'timestamp': time.time()}],
            'timestamp': time.time(),
            **(initial_context if initial_context else {})
        }
        return feedback_id

    def update_status(self, feedback_id: str, status_update: Dict[str, Any]):
        """Updates the status of a tracked feedback item.

        This would typically be called by the agent environment or monitoring system
        when an agent picks up, processes, or completes a task related to the feedback.

        Args:
            feedback_id: The ID of the feedback being updated.
            status_update: A dictionary containing the status changes 
                           (e.g., {'state': 'processing', 'agent_id': '...', 'details': '...'}).
        """
        if feedback_id not in self._feedback_status:
            print(f"Warning: Received status update for untracked feedback ID: {feedback_id}")
            return

        print(f"Updating status for feedback {feedback_id}: {status_update}")
        current_status = self._feedback_status[feedback_id]
        new_state = status_update.get('state', current_status['state'])
        timestamp = time.time()
        
        # Update main status fields
        current_status.update(status_update)
        current_status['state'] = new_state # Ensure state is updated correctly
        current_status['timestamp'] = timestamp
        
        # Add to history
        history_entry = status_update.copy()
        history_entry['state'] = new_state
        history_entry['timestamp'] = timestamp
        current_status.setdefault('history', []).append(history_entry)

        # Notify subscribers (e.g., frontend via WebSocket)
        self._notify_subscribers(feedback_id, current_status)

    def get_propagation_status(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        """Returns the current status and history for a specific feedback item."""
        return self._feedback_status.get(feedback_id)

    def subscribe_to_updates(self, feedback_id: str, callback: Callable):
        """Allows a component (e.g., frontend) to subscribe to status updates for a feedback item.
        
        Args:
            feedback_id: The feedback ID to subscribe to.
            callback: The function to call when an update occurs for this feedback ID.
                      The callback will receive the full status dictionary as an argument.
        """
        if feedback_id not in self._subscribers:
            self._subscribers[feedback_id] = []
        if callback not in self._subscribers[feedback_id]:
             self._subscribers[feedback_id].append(callback)
             print(f"New subscriber added for feedback {feedback_id}")

    def unsubscribe_from_updates(self, feedback_id: str, callback: Callable):
        """Unsubscribes a component from status updates."""
        if feedback_id in self._subscribers:
            try:
                self._subscribers[feedback_id].remove(callback)
                print(f"Subscriber removed for feedback {feedback_id}")
                if not self._subscribers[feedback_id]: # Remove key if list is empty
                    del self._subscribers[feedback_id]
            except ValueError:
                print(f"Warning: Callback not found for feedback ID {feedback_id} during unsubscribe.")

    def _notify_subscribers(self, feedback_id: str, status: Dict[str, Any]):
        """Notifies all subscribers about a status update."""
        if feedback_id in self._subscribers:
            print(f"Notifying {len(self._subscribers[feedback_id])} subscribers for feedback {feedback_id}")
            for callback in self._subscribers[feedback_id]:
                try:
                    callback(status) # Call the subscriber function
                except Exception as e:
                    print(f"Error calling subscriber for feedback {feedback_id}: {e}")

    # Placeholder for listening mechanism if using an event bus/environment
    def _listen_to_environment(self):
        """(Conceptual) Listens to agent events from the environment.
           This needs specific implementation based on the message bus/environment used.
        """
        if not self._environment:
            return
        # Example pseudo-code:
        # for event in self._environment.listen():
        #     if event.type == 'agent_feedback_update':
        #         feedback_id = event.data.get('feedback_id')
        #         status_update = event.data.get('update')
        #         if feedback_id and status_update:
        #             self.update_status(feedback_id, status_update)
        pass

# Example Usage (Conceptual)
if __name__ == '__main__':
    visualizer = PropagationVisualizer()

    # Simulate a frontend component subscribing
    def frontend_update_handler(status):
        print(f"[Frontend Update] Feedback ID: {status.get('feedback_id', '?')} - New State: {status.get('state', '?')}")
        # In a real app, this would update the UI, e.g., via WebSockets

    # 1. Track new feedback
    context = {'source_artifact': 'main.py', 'components': ['func1']}
    f_id = visualizer.track_new_feedback(initial_context=context)
    visualizer.subscribe_to_updates(f_id, frontend_update_handler)
    print("\nInitial Status:", visualizer.get_propagation_status(f_id))

    # 2. Simulate agent picking up the task
    time.sleep(1)
    update1 = {'state': 'processing', 'agent_id': 'agent_coder_1', 'details': 'Analyzing code impact...'}
    visualizer.update_status(f_id, update1)
    # print("\nStatus after update 1:", visualizer.get_propagation_status(f_id))

    # 3. Simulate agent finding affected components
    time.sleep(1)
    update2 = {'affected_components': ['func1', 'class1']}
    visualizer.update_status(f_id, update2)

    # 4. Simulate agent completing the task
    time.sleep(1)
    update3 = {'state': 'completed', 'agent_id': 'agent_coder_1', 'result': 'Changes applied successfully.'}
    visualizer.update_status(f_id, update3)
    print("\nFinal Status:", visualizer.get_propagation_status(f_id))

    # 5. Unsubscribe
    visualizer.unsubscribe_from_updates(f_id, frontend_update_handler) 