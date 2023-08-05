Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var GroupListHeader = function (_a) {
    var _b = _a.withChart, withChart = _b === void 0 ? true : _b, _c = _a.narrowGroups, narrowGroups = _c === void 0 ? false : _c;
    return (<panels_1.PanelHeader disablePadding>
    <IssueWrapper>{locale_1.t('Issue')}</IssueWrapper>
    {withChart && (<ChartWrapper className={"hidden-xs hidden-sm " + (narrowGroups ? 'hidden-md' : '')}>
        {locale_1.t('Graph')}
      </ChartWrapper>)}
    <EventUserWrapper>{locale_1.t('events')}</EventUserWrapper>
    <EventUserWrapper>{locale_1.t('users')}</EventUserWrapper>
    <AssigneeWrapper className="hidden-xs hidden-sm toolbar-header">
      {locale_1.t('Assignee')}
    </AssigneeWrapper>
  </panels_1.PanelHeader>);
};
exports.default = GroupListHeader;
var Heading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-self: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-self: center;\n  margin: 0 ", ";\n"])), space_1.default(2));
var IssueWrapper = styled_1.default(Heading)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"], ["\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var EventUserWrapper = styled_1.default(Heading)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  width: 60px;\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  justify-content: flex-end;\n  width: 60px;\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var ChartWrapper = styled_1.default(Heading)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  justify-content: space-between;\n  width: 160px;\n"], ["\n  justify-content: space-between;\n  width: 160px;\n"])));
var AssigneeWrapper = styled_1.default(Heading)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n  width: 80px;\n"], ["\n  justify-content: flex-end;\n  width: 80px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=groupListHeader.jsx.map