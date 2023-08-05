Object.defineProperty(exports, "__esModule", { value: true });
exports.getMergedTasks = exports.getOnboardingTasks = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var utils_1 = require("app/components/onboardingWizard/utils");
var platformCategories_1 = require("app/data/platformCategories");
var locale_1 = require("app/locale");
var pulsingIndicator_1 = tslib_1.__importDefault(require("app/styles/pulsingIndicator"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var eventWaiter_1 = tslib_1.__importDefault(require("app/utils/eventWaiter"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
function hasPlatformWithSourceMaps(organization) {
    var projects = organization === null || organization === void 0 ? void 0 : organization.projects;
    if (!projects) {
        return false;
    }
    return projects.some(function (_a) {
        var platform = _a.platform;
        return platform && platformCategories_1.sourceMaps.includes(platform);
    });
}
function getOnboardingTasks(organization) {
    return [
        {
            task: types_1.OnboardingTaskKey.FIRST_PROJECT,
            title: locale_1.t('Create a project'),
            description: locale_1.t("Monitor in seconds by adding a simple lines of code to your project. It's as easy as microwaving leftover pizza."),
            skippable: false,
            requisites: [],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.FIRST_EVENT,
            title: locale_1.t('Capture your first error'),
            description: locale_1.t("Time to test it out. Now that you've created a project, capture your first error. We've got an example you can fiddle with."),
            skippable: false,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/install/",
            display: true,
            SupplementComponent: withProjects_1.default(withApi_1.default(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<eventWaiter_1.default api={api} organization={organization} project={projects[0]} eventType="error" onIssueReceived={function () { return !utils_1.taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </eventWaiter_1.default>) : null;
            })),
        },
        {
            task: types_1.OnboardingTaskKey.INVITE_MEMBER,
            title: locale_1.t('Invite your team'),
            description: locale_1.t('Assign issues and comment on shared errors with coworkers so you always know who to blame when sh*t hits the fan.'),
            skippable: true,
            requisites: [],
            actionType: 'action',
            action: function () { return modal_1.openInviteMembersModal({ source: 'onboarding_widget' }); },
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.SECOND_PLATFORM,
            title: locale_1.t('Create another project'),
            description: locale_1.t('Easy, right? Don’t stop at one. Set up another project to keep things running smoothly in both the frontend and backend.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.FIRST_TRANSACTION,
            title: locale_1.t('Boost performance'),
            description: locale_1.t("Don't keep users waiting. Trace transactions, investigate spans and cross-reference related issues for those mission-critical endpoints."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/performance/getting-started/',
            display: true,
            SupplementComponent: withProjects_1.default(withApi_1.default(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<eventWaiter_1.default api={api} organization={organization} project={projects[0]} eventType="transaction" onIssueReceived={function () { return !utils_1.taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </eventWaiter_1.default>) : null;
            })),
        },
        {
            task: types_1.OnboardingTaskKey.USER_CONTEXT,
            title: locale_1.t('Get more user context'),
            description: locale_1.t('Enable us to pinpoint which users are suffering from that bad code, so you can debug the problem more swiftly and maybe even apologize for it.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/error-monitoring/issue-owners/',
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.RELEASE_TRACKING,
            title: locale_1.t('Track releases'),
            description: locale_1.t('Take an in-depth look at the health of each and every release with crash analytics, errors, related issues and suspect commits.'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/release-tracking/",
            display: true,
        },
        {
            task: types_1.OnboardingTaskKey.SOURCEMAPS,
            title: locale_1.t('Upload source maps'),
            description: locale_1.t("Deminify Javascript source code to debug with context. Seeing code in it's original form will help you debunk the ghosts of errors past."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/platforms/javascript/sourcemaps/',
            display: hasPlatformWithSourceMaps(organization),
        },
        {
            task: types_1.OnboardingTaskKey.USER_REPORTS,
            title: 'User crash reports',
            description: locale_1.t('Collect user feedback when your application crashes'),
            skippable: true,
            requisites: [
                types_1.OnboardingTaskKey.FIRST_PROJECT,
                types_1.OnboardingTaskKey.FIRST_EVENT,
                types_1.OnboardingTaskKey.USER_CONTEXT,
            ],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/user-reports/",
            display: false,
        },
        {
            task: types_1.OnboardingTaskKey.ISSUE_TRACKER,
            title: locale_1.t('Set up issue tracking'),
            description: locale_1.t('Link to Sentry issues within your issue tracker'),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT, types_1.OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/plugins/",
            display: false,
        },
        {
            task: types_1.OnboardingTaskKey.ALERT_RULE,
            title: locale_1.t('Get smarter alerts'),
            description: locale_1.t("Customize alerting rules by issue or metric. You'll get the exact information you need precisely when you need it."),
            skippable: true,
            requisites: [types_1.OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/alerts/rules/",
            display: true,
        },
    ];
}
exports.getOnboardingTasks = getOnboardingTasks;
function getMergedTasks(organization) {
    var taskDescriptors = getOnboardingTasks(organization);
    var serverTasks = organization.onboardingTasks;
    // Map server task state (i.e. completed status) with tasks objects
    var allTasks = taskDescriptors.map(function (desc) {
        return (tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, desc), serverTasks.find(function (serverTask) { return serverTask.task === desc.task; })), { requisiteTasks: [] }));
    });
    // Map incomplete requisiteTasks as full task objects
    return allTasks.map(function (task) { return (tslib_1.__assign(tslib_1.__assign({}, task), { requisiteTasks: task.requisites
            .map(function (key) { return allTasks.find(function (task2) { return task2.task === key; }); })
            .filter(function (reqTask) { return reqTask.status !== 'complete'; }) })); });
}
exports.getMergedTasks = getMergedTasks;
var PulsingIndicator = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  margin-right: ", ";\n"], ["\n  ", ";\n  margin-right: ", ";\n"])), pulsingIndicator_1.default, space_1.default(1));
var EventWaitingIndicator = styled_1.default(function (p) { return (<div {...p}>
    <PulsingIndicator />
    {locale_1.t('Waiting for event')}
  </div>); })(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-grow: 1;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  flex-grow: 1;\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.orange400; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=taskConfig.jsx.map