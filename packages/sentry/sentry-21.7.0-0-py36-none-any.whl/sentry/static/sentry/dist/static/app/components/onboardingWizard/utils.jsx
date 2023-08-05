Object.defineProperty(exports, "__esModule", { value: true });
exports.findUpcomingTasks = exports.findActiveTasks = exports.findCompleteTasks = exports.taskIsDone = void 0;
var taskIsDone = function (task) {
    return ['complete', 'skipped'].includes(task.status);
};
exports.taskIsDone = taskIsDone;
var findCompleteTasks = function (task) {
    return task.completionSeen && ['complete', 'skipped'].includes(task.status);
};
exports.findCompleteTasks = findCompleteTasks;
var findActiveTasks = function (task) {
    return task.requisiteTasks.length === 0 && !exports.findCompleteTasks(task);
};
exports.findActiveTasks = findActiveTasks;
var findUpcomingTasks = function (task) {
    return task.requisiteTasks.length > 0 && !exports.findCompleteTasks(task);
};
exports.findUpcomingTasks = findUpcomingTasks;
//# sourceMappingURL=utils.jsx.map