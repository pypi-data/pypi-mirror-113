Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var moment_1 = tslib_1.__importDefault(require("moment"));
var navigation_1 = require("app/actionCreators/navigation");
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var card_1 = tslib_1.__importDefault(require("app/components/card"));
var letterAvatar_1 = tslib_1.__importDefault(require("app/components/letterAvatar"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var testableTransition_1 = tslib_1.__importDefault(require("app/utils/testableTransition"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var skipConfirm_1 = tslib_1.__importDefault(require("./skipConfirm"));
var utils_1 = require("./utils");
var recordAnalytics = function (task, organization, action) {
    return analytics_1.trackAnalyticsEvent({
        eventKey: 'onboarding.wizard_clicked',
        eventName: 'Onboarding Wizard Clicked',
        organization_id: organization.id,
        todo_id: task.task,
        todo_title: task.title,
        action: action,
    });
};
function Task(_a) {
    var router = _a.router, task = _a.task, onSkip = _a.onSkip, onMarkComplete = _a.onMarkComplete, forwardedRef = _a.forwardedRef, organization = _a.organization;
    var handleSkip = function () {
        recordAnalytics(task, organization, 'skipped');
        onSkip(task.task);
    };
    var handleClick = function (e) {
        recordAnalytics(task, organization, 'clickthrough');
        e.stopPropagation();
        if (task.actionType === 'external') {
            window.open(task.location, '_blank');
        }
        if (task.actionType === 'action') {
            task.action();
        }
        if (task.actionType === 'app') {
            navigation_1.navigateTo(task.location + "?onboardingTask", router);
        }
    };
    if (utils_1.taskIsDone(task) && task.completionSeen) {
        var completedOn = moment_1.default(task.dateCompleted);
        return (<TaskCard ref={forwardedRef} onClick={handleClick}>
        <CompleteTitle>
          <StatusIndicator>
            {task.status === 'complete' && <CompleteIndicator />}
            {task.status === 'skipped' && <SkippedIndicator />}
          </StatusIndicator>
          {task.title}
          <DateCompleted title={completedOn.toString()}>
            {completedOn.fromNow()}
          </DateCompleted>
          {task.user ? (<TaskUserAvatar hasTooltip user={task.user}/>) : (<tooltip_1.default containerDisplayMode="inherit" title={locale_1.t('No user was associated with completing this task')}>
              <TaskBlankAvatar round/>
            </tooltip_1.default>)}
        </CompleteTitle>
      </TaskCard>);
    }
    var IncompleteMarker = task.requisiteTasks.length > 0 && (<tooltip_1.default containerDisplayMode="block" title={locale_1.tct('[requisite] before completing this task', {
            requisite: task.requisiteTasks[0].title,
        })}>
      <icons_1.IconLock color="orange400"/>
    </tooltip_1.default>);
    var SupplementComponent = task.SupplementComponent;
    var supplement = SupplementComponent && (<SupplementComponent task={task} onCompleteTask={function () { return onMarkComplete(task.task); }}/>);
    var skipAction = task.skippable && (<skipConfirm_1.default onSkip={handleSkip}>
      {function (_a) {
        var skip = _a.skip;
        return <StyledIconClose size="xs" onClick={skip}/>;
    }}
    </skipConfirm_1.default>);
    return (<TaskCard interactive ref={forwardedRef} onClick={handleClick} data-test-id={task.task}>
      <IncompleteTitle>
        {IncompleteMarker}
        {task.title}
      </IncompleteTitle>
      <Description>{"" + task.description}</Description>
      {task.requisiteTasks.length === 0 && (<ActionBar>
          {skipAction}
          {supplement}
          {task.status === 'pending' ? (<InProgressIndicator user={task.user}/>) : (<button_1.default priority="primary" size="small">
              {locale_1.t('Start')}
            </button_1.default>)}
        </ActionBar>)}
    </TaskCard>);
}
var TaskCard = styled_1.default(card_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  padding: ", " ", ";\n"], ["\n  position: relative;\n  padding: ", " ", ";\n"])), space_1.default(2), space_1.default(3));
var IncompleteTitle = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-weight: 600;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-weight: 600;\n"])), space_1.default(1));
var CompleteTitle = styled_1.default(IncompleteTitle)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: min-content 1fr max-content min-content;\n"], ["\n  grid-template-columns: min-content 1fr max-content min-content;\n"])));
var Description = styled_1.default('p')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  margin: ", " 0 0 0;\n"], ["\n  font-size: ", ";\n  color: ", ";\n  margin: ", " 0 0 0;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, space_1.default(0.5));
var ActionBar = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-end;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-end;\n  margin-top: ", ";\n"])), space_1.default(1.5));
var InProgressIndicator = styled_1.default(function (_a) {
    var user = _a.user, props = tslib_1.__rest(_a, ["user"]);
    return (<div {...props}>
    <tooltip_1.default disabled={!user} containerDisplayMode="flex" title={locale_1.tct('This task has been started by [user]', {
            user: user === null || user === void 0 ? void 0 : user.name,
        })}>
      <icons_1.IconSync />
    </tooltip_1.default>
    {locale_1.t('Task in progress...')}
  </div>);
})(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.orange400; }, space_1.default(1));
var StyledIconClose = styled_1.default(icons_1.IconClose)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  right: ", ";\n  top: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  right: ", ";\n  top: ", ";\n  color: ", ";\n"])), space_1.default(1.5), space_1.default(1.5), function (p) { return p.theme.gray300; });
var transition = testableTransition_1.default();
var StatusIndicator = styled_1.default(framer_motion_1.motion.div)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
StatusIndicator.defaultProps = {
    variants: {
        initial: { opacity: 0, x: 10 },
        animate: { opacity: 1, x: 0 },
    },
    transition: transition,
};
var CompleteIndicator = styled_1.default(icons_1.IconCheckmark)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject([""], [""])));
CompleteIndicator.defaultProps = {
    isCircled: true,
    color: 'green300',
};
var SkippedIndicator = styled_1.default(icons_1.IconClose)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject([""], [""])));
SkippedIndicator.defaultProps = {
    isCircled: true,
    color: 'orange400',
};
var completedItemAnimation = {
    initial: { opacity: 0, x: -10 },
    animate: { opacity: 1, x: 0 },
};
var DateCompleted = styled_1.default(framer_motion_1.motion.div)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 300;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 300;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
DateCompleted.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskUserAvatar = framer_motion_1.motion(avatar_1.default);
TaskUserAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskBlankAvatar = styled_1.default(framer_motion_1.motion(letterAvatar_1.default))(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  position: unset;\n"], ["\n  position: unset;\n"])));
TaskBlankAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var WrappedTask = withOrganization_1.default(ReactRouter.withRouter(Task));
exports.default = React.forwardRef(function (props, ref) { return <WrappedTask forwardedRef={ref} {...props}/>; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=task.jsx.map