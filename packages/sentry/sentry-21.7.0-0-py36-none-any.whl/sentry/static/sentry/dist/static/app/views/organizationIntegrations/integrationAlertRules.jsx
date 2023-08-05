Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var IntegrationAlertRules = function (_a) {
    var projects = _a.projects, organization = _a.organization;
    return (<panels_1.Panel>
    <panels_1.PanelHeader>{locale_1.t('Project Configuration')}</panels_1.PanelHeader>
    <panels_1.PanelBody>
      {projects.length === 0 && (<emptyMessage_1.default size="large">
          {locale_1.t('You have no projects to add Alert Rules to')}
        </emptyMessage_1.default>)}
      {projects.map(function (project) { return (<ProjectItem key={project.slug}>
          <projectBadge_1.default project={project} avatarSize={16}/>
          <button_1.default to={"/organizations/" + organization.slug + "/alerts/" + project.slug + "/wizard/"} size="xsmall">
            {locale_1.t('Add Alert Rule')}
          </button_1.default>
        </ProjectItem>); })}
    </panels_1.PanelBody>
  </panels_1.Panel>);
};
var ProjectItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
exports.default = withOrganization_1.default(withProjects_1.default(IntegrationAlertRules));
var templateObject_1;
//# sourceMappingURL=integrationAlertRules.jsx.map