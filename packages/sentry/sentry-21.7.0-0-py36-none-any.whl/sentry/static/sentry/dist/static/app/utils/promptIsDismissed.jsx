Object.defineProperty(exports, "__esModule", { value: true });
exports.promptCanShow = exports.promptIsDismissed = void 0;
var promptsActivity_1 = require("./promptsActivity");
var promptIsDismissed = function (prompt, daysToSnooze) {
    if (daysToSnooze === void 0) { daysToSnooze = 14; }
    var _a = prompt || {}, snoozedTime = _a.snoozedTime, dismissedTime = _a.dismissedTime;
    // check if the prompt has been dismissed
    if (dismissedTime) {
        return true;
    }
    // check if it has been snoozed
    return !snoozedTime ? false : promptsActivity_1.snoozedDays(snoozedTime) < daysToSnooze;
};
exports.promptIsDismissed = promptIsDismissed;
function promptCanShow(prompt, uuid) {
    /**
     * This is to ensure that only one of suspect_commits
     * or distributed_tracing is shown at a given time.
     */
    var x = (parseInt(uuid.charAt(0), 16) || 0) % 2;
    if (prompt === 'suspect_commits') {
        return x === 1;
    }
    else if (prompt === 'distributed_tracing') {
        return x === 0;
    }
    else {
        return true;
    }
}
exports.promptCanShow = promptCanShow;
//# sourceMappingURL=promptIsDismissed.jsx.map