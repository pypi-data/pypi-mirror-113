Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var accountNotificationSettings_1 = require("app/data/forms/accountNotificationSettings");
var locale_1 = require("app/locale");
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var fields_1 = require("app/views/settings/account/notifications/fields");
var notificationSettingsByType_1 = tslib_1.__importDefault(require("app/views/settings/account/notifications/notificationSettingsByType"));
var utils_1 = require("app/views/settings/account/notifications/utils");
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var PanelBodyLineItem = styled_1.default(panels_1.PanelBody)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; });
var AccountNotificationsByProject = function (_a) {
    var projects = _a.projects, field = _a.field;
    var projectsByOrg = utils_1.groupByOrganization(projects);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = tslib_1.__rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = Object.values(projectsByOrg).map(function (org) { return ({
        name: org.organization.name,
        projects: org.projects.map(function (project) { return (tslib_1.__assign(tslib_1.__assign({}, fieldConfig), { 
            // `name` key refers to field name
            // we use project.id because slugs are not unique across orgs
            name: project.id, label: project.slug })); }),
    }); });
    return (<react_1.Fragment>
      {data.map(function (_a) {
            var name = _a.name, projectFields = _a.projects;
            return (<div key={name}>
          <panels_1.PanelHeader>{name}</panels_1.PanelHeader>
          {projectFields.map(function (f) { return (<PanelBodyLineItem key={f.name}>
              <selectField_1.default defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
            </PanelBodyLineItem>); })}
        </div>);
        })}
    </react_1.Fragment>);
};
var AccountNotificationsByOrganization = function (_a) {
    var organizations = _a.organizations, field = _a.field;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = tslib_1.__rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = organizations.map(function (org) { return (tslib_1.__assign(tslib_1.__assign({}, fieldConfig), { 
        // `name` key refers to field name
        // we use org.id to remain consistent project.id use (which is required because slugs are not unique across orgs)
        name: org.id, label: org.slug })); });
    return (<react_1.Fragment>
      {data.map(function (f) { return (<PanelBodyLineItem key={f.name}>
          <selectField_1.default defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
        </PanelBodyLineItem>); })}
    </react_1.Fragment>);
};
var AccountNotificationsByOrganizationContainer = withOrganizations_1.default(AccountNotificationsByOrganization);
var AccountNotificationFineTuning = /** @class */ (function (_super) {
    tslib_1.__extends(AccountNotificationFineTuning, _super);
    function AccountNotificationFineTuning() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountNotificationFineTuning.prototype.getEndpoints = function () {
        var fineTuneType = this.props.params.fineTuneType;
        var endpoints = [
            ['notifications', '/users/me/notifications/'],
            ['fineTuneData', "/users/me/notifications/" + fineTuneType + "/"],
        ];
        if (utils_1.isGroupedByProject(fineTuneType)) {
            endpoints.push(['projects', '/projects/']);
        }
        endpoints.push(['emails', '/users/me/emails/']);
        if (fineTuneType === 'email') {
            endpoints.push(['emails', '/users/me/emails/']);
        }
        return endpoints;
    };
    Object.defineProperty(AccountNotificationFineTuning.prototype, "emailChoices", {
        // Return a sorted list of user's verified emails
        get: function () {
            var _a, _b, _c;
            return ((_c = (_b = (_a = this.state.emails) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                var isVerified = _a.isVerified;
                return isVerified;
            })) === null || _b === void 0 ? void 0 : _b.sort(function (a, b) {
                // Sort by primary -> email
                if (a.isPrimary) {
                    return -1;
                }
                else if (b.isPrimary) {
                    return 1;
                }
                return a.email < b.email ? -1 : 1;
            })) !== null && _c !== void 0 ? _c : []);
        },
        enumerable: false,
        configurable: true
    });
    AccountNotificationFineTuning.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organizations = _a.organizations;
        var fineTuneType = params.fineTuneType;
        if (['alerts', 'deploy', 'workflow'].includes(fineTuneType) &&
            organizations.some(function (organization) {
                return organization.features.includes('notification-platform');
            })) {
            return <notificationSettingsByType_1.default notificationType={fineTuneType}/>;
        }
        var _b = this.state, notifications = _b.notifications, projects = _b.projects, fineTuneData = _b.fineTuneData, projectsPageLinks = _b.projectsPageLinks;
        var isProject = utils_1.isGroupedByProject(fineTuneType);
        var field = fields_1.ACCOUNT_NOTIFICATION_FIELDS[fineTuneType];
        var title = field.title, description = field.description;
        var _c = tslib_1.__read(isProject ? this.getEndpoints()[2] : [], 2), stateKey = _c[0], url = _c[1];
        var hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length);
        if (fineTuneType === 'email') {
            // Fetch verified email addresses
            field.choices = this.emailChoices.map(function (_a) {
                var email = _a.email;
                return [email, email];
            });
        }
        if (!notifications || !fineTuneData) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={title}/>
        {description && <textBlock_1.default>{description}</textBlock_1.default>}

        {field &&
                field.defaultFieldName &&
                // not implemented yet
                field.defaultFieldName !== 'weeklyReports' && (<form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/" initialData={notifications}>
              <jsonForm_1.default title={"Default " + title} fields={[accountNotificationSettings_1.fields[field.defaultFieldName]]}/>
            </form_1.default>)}
        <panels_1.Panel>
          <panels_1.PanelBody>
            <panels_1.PanelHeader hasButtons={isProject}>
              <Heading>{isProject ? locale_1.t('Projects') : locale_1.t('Organizations')}</Heading>
              <div>
                {isProject &&
                this.renderSearchInput({
                    placeholder: locale_1.t('Search Projects'),
                    url: url,
                    stateKey: stateKey,
                })}
              </div>
            </panels_1.PanelHeader>

            <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint={"/users/me/notifications/" + fineTuneType + "/"} initialData={fineTuneData}>
              {isProject && hasProjects && (<AccountNotificationsByProject projects={projects} field={field}/>)}

              {isProject && !hasProjects && (<emptyMessage_1.default>{locale_1.t('No projects found')}</emptyMessage_1.default>)}

              {!isProject && (<AccountNotificationsByOrganizationContainer field={field}/>)}
            </form_1.default>
          </panels_1.PanelBody>
        </panels_1.Panel>

        {projects && <pagination_1.default pageLinks={projectsPageLinks} {...this.props}/>}
      </div>);
    };
    return AccountNotificationFineTuning;
}(asyncView_1.default));
var Heading = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
exports.default = withOrganizations_1.default(AccountNotificationFineTuning);
var templateObject_1, templateObject_2;
//# sourceMappingURL=accountNotificationFineTuning.jsx.map