Object.defineProperty(exports, "__esModule", { value: true });
exports.OrgSummary = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var organizationAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/organizationAvatar"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var SidebarOrgSummary = function (_a) {
    var organization = _a.organization;
    var fullOrg = organization;
    var projects = fullOrg.projects && fullOrg.projects.length;
    var extra = [];
    if (projects) {
        extra.push(locale_1.tn('%s project', '%s projects', projects));
    }
    return (<OrgSummary>
      <organizationAvatar_1.default organization={organization} size={36}/>

      <Details>
        <SummaryOrgName>{organization.name}</SummaryOrgName>
        {!!extra.length && <SummaryOrgDetails>{extra.join(', ')}</SummaryOrgDetails>}
      </Details>
    </OrgSummary>);
};
var OrgSummary = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: 10px 15px;\n  overflow: hidden;\n"], ["\n  display: flex;\n  padding: 10px 15px;\n  overflow: hidden;\n"])));
exports.OrgSummary = OrgSummary;
var SummaryOrgName = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 16px;\n  line-height: 1.1;\n  font-weight: bold;\n  margin-bottom: 4px;\n  ", ";\n"], ["\n  color: ", ";\n  font-size: 16px;\n  line-height: 1.1;\n  font-weight: bold;\n  margin-bottom: 4px;\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var SummaryOrgDetails = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 14px;\n  line-height: 1;\n  ", ";\n"], ["\n  color: ", ";\n  font-size: 14px;\n  line-height: 1;\n  ", ";\n"])), function (p) { return p.theme.subText; }, overflowEllipsis_1.default);
var Details = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  padding-left: 10px;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n\n  padding-left: 10px;\n  overflow: hidden;\n"])));
exports.default = SidebarOrgSummary;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sidebarOrgSummary.jsx.map