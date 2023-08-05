Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var highlight_top_right_svg_1 = tslib_1.__importDefault(require("sentry-images/pattern/highlight-top-right.svg"));
var onboardingTasks_1 = require("app/actionCreators/onboardingTasks");
var sidebarPanel_1 = tslib_1.__importDefault(require("app/components/sidebar/sidebarPanel"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var progressHeader_1 = tslib_1.__importDefault(require("./progressHeader"));
var task_1 = tslib_1.__importDefault(require("./task"));
var taskConfig_1 = require("./taskConfig");
var utils_1 = require("./utils");
/**
 * How long (in ms) to delay before beginning to mark tasks complete
 */
var INITIAL_MARK_COMPLETE_TIMEOUT = 600;
/**
 * How long (in ms) to delay between marking each unseen task as complete.
 */
var COMPLETION_SEEN_TIMEOUT = 800;
var doTimeout = function (timeout) {
    return new Promise(function (resolve) { return setTimeout(resolve, timeout); });
};
var Heading = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  font-size: ", ";\n  text-transform: uppercase;\n  font-weight: 600;\n  line-height: 1;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  color: ", ";\n  font-size: ", ";\n  text-transform: uppercase;\n  font-weight: 600;\n  line-height: 1;\n  margin-top: ", ";\n"])), function (p) { return p.theme.purple300; }, function (p) { return p.theme.fontSizeExtraSmall; }, space_1.default(3));
Heading.defaultProps = {
    layout: true,
    transition: testableTransition_1.default(),
};
var completeNowHeading = <Heading key="now">{locale_1.t('The Basics')}</Heading>;
var upcomingTasksHeading = (<Heading key="upcoming">
    <tooltip_1.default containerDisplayMode="block" title={locale_1.t('Some tasks should be completed before completing these tasks')}>
      {locale_1.t('Level Up')}
    </tooltip_1.default>
  </Heading>);
var completedTasksHeading = <Heading key="complete">{locale_1.t('Completed')}</Heading>;
var OnboardingWizardSidebar = /** @class */ (function (_super) {
    tslib_1.__extends(OnboardingWizardSidebar, _super);
    function OnboardingWizardSidebar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.makeTaskUpdater = function (status) { return function (task) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            onboardingTasks_1.updateOnboardingTask(api, organization, { task: task, status: status, completionSeen: true });
        }; };
        _this.renderItem = function (task) { return (<AnimatedTaskItem task={task} key={"" + task.task} onSkip={_this.makeTaskUpdater('skipped')} onMarkComplete={_this.makeTaskUpdater('complete')}/>); };
        return _this;
    }
    OnboardingWizardSidebar.prototype.componentDidMount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: 
                    // Add a minor delay to marking tasks complete to account for the animation
                    // opening of the sidebar panel
                    return [4 /*yield*/, doTimeout(INITIAL_MARK_COMPLETE_TIMEOUT)];
                    case 1:
                        // Add a minor delay to marking tasks complete to account for the animation
                        // opening of the sidebar panel
                        _a.sent();
                        this.markTasksAsSeen();
                        return [2 /*return*/];
                }
            });
        });
    };
    OnboardingWizardSidebar.prototype.markTasksAsSeen = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var unseenTasks, unseenTasks_1, unseenTasks_1_1, task, _a, api, organization, e_1_1;
            var e_1, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        unseenTasks = this.segmentedTasks.all
                            .filter(function (task) { return utils_1.taskIsDone(task) && !task.completionSeen; })
                            .map(function (task) { return task.task; });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 6, 7, 8]);
                        unseenTasks_1 = tslib_1.__values(unseenTasks), unseenTasks_1_1 = unseenTasks_1.next();
                        _c.label = 2;
                    case 2:
                        if (!!unseenTasks_1_1.done) return [3 /*break*/, 5];
                        task = unseenTasks_1_1.value;
                        return [4 /*yield*/, doTimeout(COMPLETION_SEEN_TIMEOUT)];
                    case 3:
                        _c.sent();
                        _a = this.props, api = _a.api, organization = _a.organization;
                        onboardingTasks_1.updateOnboardingTask(api, organization, {
                            task: task,
                            completionSeen: true,
                        });
                        _c.label = 4;
                    case 4:
                        unseenTasks_1_1 = unseenTasks_1.next();
                        return [3 /*break*/, 2];
                    case 5: return [3 /*break*/, 8];
                    case 6:
                        e_1_1 = _c.sent();
                        e_1 = { error: e_1_1 };
                        return [3 /*break*/, 8];
                    case 7:
                        try {
                            if (unseenTasks_1_1 && !unseenTasks_1_1.done && (_b = unseenTasks_1.return)) _b.call(unseenTasks_1);
                        }
                        finally { if (e_1) throw e_1.error; }
                        return [7 /*endfinally*/];
                    case 8: return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(OnboardingWizardSidebar.prototype, "segmentedTasks", {
        get: function () {
            var organization = this.props.organization;
            var all = taskConfig_1.getMergedTasks(organization).filter(function (task) { return task.display; });
            var active = all.filter(utils_1.findActiveTasks);
            var upcoming = all.filter(utils_1.findUpcomingTasks);
            var complete = all.filter(utils_1.findCompleteTasks);
            return { active: active, upcoming: upcoming, complete: complete, all: all };
        },
        enumerable: false,
        configurable: true
    });
    OnboardingWizardSidebar.prototype.render = function () {
        var _a = this.props, collapsed = _a.collapsed, orientation = _a.orientation, onClose = _a.onClose;
        var _b = this.segmentedTasks, all = _b.all, active = _b.active, upcoming = _b.upcoming, complete = _b.complete;
        var completeList = (<CompleteList key="complete-group">
        <framer_motion_1.AnimatePresence initial={false}>{complete.map(this.renderItem)}</framer_motion_1.AnimatePresence>
      </CompleteList>);
        var items = tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([
            active.length > 0 && completeNowHeading
        ], tslib_1.__read(active.map(this.renderItem))), [
            upcoming.length > 0 && upcomingTasksHeading
        ]), tslib_1.__read(upcoming.map(this.renderItem))), [
            complete.length > 0 && completedTasksHeading,
            completeList,
        ]);
        return (<TaskSidebarPanel collapsed={collapsed} hidePanel={onClose} orientation={orientation}>
        <TopRight src={highlight_top_right_svg_1.default}/>
        <progressHeader_1.default allTasks={all} completedTasks={complete}/>
        <TaskList>
          <framer_motion_1.AnimatePresence initial={false}>{items}</framer_motion_1.AnimatePresence>
        </TaskList>
      </TaskSidebarPanel>);
    };
    return OnboardingWizardSidebar;
}(react_1.Component));
var TaskSidebarPanel = styled_1.default(sidebarPanel_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 450px;\n"], ["\n  width: 450px;\n"])));
var AnimatedTaskItem = framer_motion_1.motion(task_1.default);
AnimatedTaskItem.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    layout: true,
    variants: {
        initial: {
            opacity: 0,
            y: 40,
        },
        animate: {
            opacity: 1,
            y: 0,
            transition: testableTransition_1.default({
                delay: 0.8,
                when: 'beforeChildren',
                staggerChildren: 0.3,
            }),
        },
        exit: {
            y: 20,
            z: -10,
            opacity: 0,
            transition: { duration: 0.2 },
        },
    },
};
var TaskList = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  margin: ", " ", " ", " ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  margin: ", " ", " ", " ", ";\n"])), space_1.default(1), space_1.default(1), space_1.default(4), space_1.default(4), space_1.default(4));
var CompleteList = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: row;\n\n  > div {\n    transition: border-radius 500ms;\n  }\n\n  > div:not(:first-of-type) {\n    margin-top: -1px;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n\n  > div:not(:last-of-type) {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: row;\n\n  > div {\n    transition: border-radius 500ms;\n  }\n\n  > div:not(:first-of-type) {\n    margin-top: -1px;\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n\n  > div:not(:last-of-type) {\n    border-bottom-left-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"])));
var TopRight = styled_1.default('img')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n  width: 60%;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n  width: 60%;\n"])));
exports.default = withApi_1.default(withOrganization_1.default(OnboardingWizardSidebar));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebar.jsx.map