Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function ProcessingIssueHint(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, issue = _a.issue, showProject = _a.showProject;
    var link = "/settings/" + orgId + "/projects/" + projectId + "/processing-issues/";
    var showButton = false;
    var text = '';
    var lastEvent = null;
    var icon = null;
    var alertType = 'error';
    var project = null;
    if (showProject) {
        project = (<React.Fragment>
        <strong>{projectId}</strong> &mdash;{' '}
      </React.Fragment>);
    }
    if (issue.numIssues > 0) {
        icon = <icons_1.IconWarning size="sm" color="red300"/>;
        text = locale_1.tn('There is %s issue blocking event processing', 'There are %s issues blocking event processing', issue.numIssues);
        lastEvent = (<React.Fragment>
        (
        {locale_1.tct('last event from [ago]', {
                ago: <timeSince_1.default date={issue.lastSeen}/>,
            })}
        )
      </React.Fragment>);
        alertType = 'error';
        showButton = true;
    }
    else if (issue.issuesProcessing > 0) {
        icon = <icons_1.IconSettings size="sm" color="blue300"/>;
        alertType = 'info';
        text = locale_1.tn('Reprocessing %s event …', 'Reprocessing %s events …', issue.issuesProcessing);
    }
    else if (issue.resolveableIssues > 0) {
        icon = <icons_1.IconSettings size="sm" color="yellow300"/>;
        alertType = 'warning';
        text = locale_1.tn('There is %s event pending reprocessing.', 'There are %s events pending reprocessing.', issue.resolveableIssues);
        showButton = true;
    }
    else {
        /* we should not go here but what do we know */
        return null;
    }
    return (<StyledAlert type={alertType} icon={icon}>
      <Wrapper>
        <div>
          {project} <strong>{text}</strong> {lastEvent}
        </div>
        {showButton && (<div>
            <StyledButton size="xsmall" to={link}>
              {locale_1.t('Show details')}
            </StyledButton>
          </div>)}
      </Wrapper>
    </StyledAlert>);
}
exports.default = ProcessingIssueHint;
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-width: 1px 0;\n  border-radius: 0;\n  margin: 0;\n  font-size: ", ";\n"], ["\n  border-width: 1px 0;\n  border-radius: 0;\n  margin: 0;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var StyledButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  margin-left: ", ";\n"], ["\n  white-space: nowrap;\n  margin-left: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=processingIssueHint.jsx.map