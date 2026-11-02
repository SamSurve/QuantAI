/**
 * QuantAI Research Client Orchestrator
 * Manages request sequencing, stale-response rejection, and active controller abortion.
 */

(function () {
  'use strict';

  var currentSequenceId = 0;
  var activeController = null;

  function cancelInFlight() {
    if (activeController) {
      activeController.abort();
      activeController = null;
    }
  }

  function startResearchSequence() {
    cancelInFlight();
    currentSequenceId += 1;
    activeController = new AbortController();
    return {
      sequenceId: currentSequenceId,
      controller: activeController,
      signal: activeController.signal,
    };
  }

  function isLatestSequence(sequenceId) {
    return sequenceId === currentSequenceId;
  }

  window.QuantAIResearch = {
    startSequence: startResearchSequence,
    cancelInFlight: cancelInFlight,
    isLatestSequence: isLatestSequence,
    getCurrentSequenceId: function () {
      return currentSequenceId;
    },
  };
})();
