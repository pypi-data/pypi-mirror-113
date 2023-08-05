Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("./types");
function AlertBadge(_a) {
    var status = _a.status, _b = _a.hideText, hideText = _b === void 0 ? false : _b, isIssue = _a.isIssue;
    var statusText = locale_1.t('Resolved');
    var Icon = icons_1.IconCheckmark;
    var color = 'green300';
    if (isIssue) {
        statusText = locale_1.t('Issue');
        Icon = icons_1.IconIssues;
        color = 'gray300';
    }
    else if (status === types_1.IncidentStatus.CRITICAL) {
        statusText = locale_1.t('Critical');
        Icon = icons_1.IconFire;
        color = 'red300';
    }
    else if (status === types_1.IncidentStatus.WARNING) {
        statusText = locale_1.t('Warning');
        Icon = icons_1.IconWarning;
        color = 'yellow300';
    }
    return (<Wrapper displayFlex={!hideText}>
      <AlertIconWrapper color={color} icon={Icon}>
        <Icon color="white"/>
      </AlertIconWrapper>

      {!hideText && <IncidentStatusValue color={color}>{statusText}</IncidentStatusValue>}
    </Wrapper>);
}
exports.default = AlertBadge;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: ", ";\n  align-items: center;\n"], ["\n  display: ", ";\n  align-items: center;\n"])), function (p) { return (p.displayFlex ? "flex" : "block"); });
var AlertIconWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n  min-width: 30px;\n\n  &:before {\n    content: '';\n    position: absolute;\n    width: 22px;\n    height: 22px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n\n  svg {\n    width: ", ";\n    z-index: 1;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n  min-width: 30px;\n\n  &:before {\n    content: '';\n    position: absolute;\n    width: 22px;\n    height: 22px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n\n  svg {\n    width: ", ";\n    z-index: 1;\n  }\n"])), function (p) { return (p.icon === icons_1.IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme[p.color]; }, function (p) { return (p.icon === icons_1.IconIssues ? '11px' : '13px'); });
var IncidentStatusValue = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme[p.color]; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=alertBadge.jsx.map