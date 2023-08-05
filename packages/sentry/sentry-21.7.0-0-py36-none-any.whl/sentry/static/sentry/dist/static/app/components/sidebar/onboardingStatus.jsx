Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sidebar_1 = tslib_1.__importDefault(require("app/components/onboardingWizard/sidebar"));
var taskConfig_1 = require("app/components/onboardingWizard/taskConfig");
var progressRing_1 = tslib_1.__importStar(require("app/components/progressRing"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var types_1 = require("./types");
var isDone = function (task) {
    return task.status === 'complete' || task.status === 'skipped';
};
var progressTextCss = function () { return react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n"])), theme_1.default.fontSizeMedium); };
var OnboardingStatus = /** @class */ (function (_super) {
    tslib_1.__extends(OnboardingStatus, _super);
    function OnboardingStatus() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleShowPanel = function () {
            var _a = _this.props, org = _a.org, onShowPanel = _a.onShowPanel;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'onboarding.wizard_opened',
                eventName: 'Onboarding Wizard Opened',
                organization_id: org.id,
            });
            onShowPanel();
        };
        return _this;
    }
    OnboardingStatus.prototype.render = function () {
        var _a = this.props, collapsed = _a.collapsed, org = _a.org, currentPanel = _a.currentPanel, orientation = _a.orientation, hidePanel = _a.hidePanel;
        if (!(org.features && org.features.includes('onboarding'))) {
            return null;
        }
        var tasks = taskConfig_1.getMergedTasks(org);
        var allDisplayedTasks = tasks.filter(function (task) { return task.display; });
        var doneTasks = allDisplayedTasks.filter(isDone);
        var numberRemaining = allDisplayedTasks.length - doneTasks.length;
        var pendingCompletionSeen = doneTasks.some(function (task) {
            return allDisplayedTasks.some(function (displayedTask) { return displayedTask.task === task.task; }) &&
                task.status === 'complete' &&
                !task.completionSeen;
        });
        var isActive = currentPanel === types_1.SidebarPanelKey.OnboardingWizard;
        if (doneTasks.length >= allDisplayedTasks.length && !isActive) {
            return null;
        }
        return (<react_1.Fragment>
        <Container onClick={this.handleShowPanel} isActive={isActive}>
          <progressRing_1.default animateText textCss={progressTextCss} text={allDisplayedTasks.length - doneTasks.length} value={(doneTasks.length / allDisplayedTasks.length) * 100} backgroundColor="rgba(255, 255, 255, 0.15)" progressEndcaps="round" size={38} barWidth={6}/>
          {!collapsed && (<div>
              <Heading>{locale_1.t('Quick Start')}</Heading>
              <Remaining>
                {locale_1.tct('[numberRemaining] Remaining tasks', { numberRemaining: numberRemaining })}
                {pendingCompletionSeen && <PendingSeenIndicator />}
              </Remaining>
            </div>)}
        </Container>
        {isActive && (<sidebar_1.default orientation={orientation} collapsed={collapsed} onClose={hidePanel}/>)}
      </react_1.Fragment>);
    };
    return OnboardingStatus;
}(react_1.Component));
var Heading = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray200; }, space_1.default(0.25));
var Remaining = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  transition: color 100ms;\n  font-size: ", ";\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space_1.default(0.75));
var PendingSeenIndicator = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border-radius: 50%;\n  height: 7px;\n  width: 7px;\n"], ["\n  background: ", ";\n  border-radius: 50%;\n  height: 7px;\n  width: 7px;\n"])), function (p) { return p.theme.red300; });
var hoverCss = function (p) { return react_2.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  background: rgba(255, 255, 255, 0.05);\n\n  ", " {\n    stroke: rgba(255, 255, 255, 0.3);\n  }\n  ", " {\n    stroke: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n"], ["\n  background: rgba(255, 255, 255, 0.05);\n\n  ", " {\n    stroke: rgba(255, 255, 255, 0.3);\n  }\n  ", " {\n    stroke: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n\n  ", " {\n    color: ", ";\n  }\n  ", " {\n    color: ", ";\n  }\n"])), progressRing_1.RingBackground, progressRing_1.RingBar, p.theme.green200, progressRing_1.RingText, p.theme.white, Heading, p.theme.white, Remaining, p.theme.gray200); };
var Container = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  padding: 9px 19px 9px 16px;\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  transition: background 100ms;\n\n  ", ";\n\n  &:hover {\n    ", ";\n  }\n"], ["\n  padding: 9px 19px 9px 16px;\n  cursor: pointer;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  transition: background 100ms;\n\n  ", ";\n\n  &:hover {\n    ", ";\n  }\n"])), space_1.default(1.5), function (p) { return p.isActive && hoverCss(p); }, hoverCss);
exports.default = OnboardingStatus;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=onboardingStatus.jsx.map