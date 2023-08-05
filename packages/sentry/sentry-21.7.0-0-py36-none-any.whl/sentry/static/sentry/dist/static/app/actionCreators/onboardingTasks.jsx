Object.defineProperty(exports, "__esModule", { value: true });
exports.updateOnboardingTask = void 0;
var tslib_1 = require("tslib");
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
/**
 * Update an onboarding task.
 *
 * If no API client is provided the task will not be updated on the server side
 * and will only update in the organization store.
 */
function updateOnboardingTask(api, organization, updatedTask) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var hasExistingTask, user, onboardingTasks;
        return tslib_1.__generator(this, function (_a) {
            if (api !== null) {
                api.requestPromise("/organizations/" + organization.slug + "/onboarding-tasks/", {
                    method: 'POST',
                    data: updatedTask,
                });
            }
            hasExistingTask = organization.onboardingTasks.find(function (task) { return task.task === updatedTask.task; });
            user = configStore_1.default.get('user');
            onboardingTasks = hasExistingTask
                ? organization.onboardingTasks.map(function (task) {
                    return task.task === updatedTask.task ? tslib_1.__assign(tslib_1.__assign({}, task), updatedTask) : task;
                })
                : tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(organization.onboardingTasks)), [tslib_1.__assign(tslib_1.__assign({}, updatedTask), { user: user })]);
            organizationActions_1.default.update({ onboardingTasks: onboardingTasks });
            return [2 /*return*/];
        });
    });
}
exports.updateOnboardingTask = updateOnboardingTask;
//# sourceMappingURL=onboardingTasks.jsx.map