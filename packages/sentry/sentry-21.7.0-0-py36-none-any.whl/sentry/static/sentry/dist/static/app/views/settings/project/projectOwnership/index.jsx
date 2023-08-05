Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var addCodeOwnerModal_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/addCodeOwnerModal"));
var codeowners_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/codeowners"));
var rulesPanel_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/rulesPanel"));
var ProjectOwnership = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectOwnership, _super);
    function ProjectOwnership() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddCodeOwner = function () {
            var _a = _this.state, codeMappings = _a.codeMappings, integrations = _a.integrations;
            modal_1.openModal(function (modalProps) { return (<addCodeOwnerModal_1.default {...modalProps} organization={_this.props.organization} project={_this.props.project} codeMappings={codeMappings} integrations={integrations} onSave={_this.handleCodeownerAdded}/>); });
        };
        _this.handleOwnershipSave = function (text) {
            _this.setState(function (prevState) { return ({
                ownership: tslib_1.__assign(tslib_1.__assign({}, prevState.ownership), { raw: text }),
            }); });
        };
        _this.handleCodeownerAdded = function (data) {
            var codeowners = _this.state.codeowners;
            var newCodeowners = codeowners === null || codeowners === void 0 ? void 0 : codeowners.concat(data);
            _this.setState({ codeowners: newCodeowners });
        };
        _this.handleCodeownerDeleted = function (data) {
            var codeowners = _this.state.codeowners;
            var newCodeowners = codeowners === null || codeowners === void 0 ? void 0 : codeowners.filter(function (codeowner) { return codeowner.id !== data.id; });
            _this.setState({ codeowners: newCodeowners });
        };
        _this.renderCodeOwnerErrors = function () {
            var _a = _this.props, project = _a.project, organization = _a.organization;
            var codeowners = _this.state.codeowners;
            var errMessageComponent = function (message, values, link, linkValue) { return (<react_1.Fragment>
        <ErrorMessageContainer>
          <span>{message}</span>
          <b>{values.join(', ')}</b>
        </ErrorMessageContainer>
        <ErrorCtaContainer>
          <externalLink_1.default href={link}>{linkValue}</externalLink_1.default>
        </ErrorCtaContainer>
      </react_1.Fragment>); };
            return (codeowners || [])
                .filter(function (_a) {
                var errors = _a.errors;
                return Object.values(errors).flat().length;
            })
                .map(function (_a) {
                var id = _a.id, codeMapping = _a.codeMapping, errors = _a.errors;
                var errMessage = function (type, values) {
                    var _a, _b;
                    switch (type) {
                        case 'missing_external_teams':
                            return errMessageComponent("The following teams do not have an association in the organization: " + organization.slug, values, "/settings/" + organization.slug + "/integrations/" + ((_a = codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.provider) === null || _a === void 0 ? void 0 : _a.slug) + "/" + (codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.integrationId) + "/?tab=teamMappings", 'Configure Team Mappings');
                        case 'missing_external_users':
                            return errMessageComponent("The following usernames do not have an association in the organization: " + organization.slug, values, "/settings/" + organization.slug + "/integrations/" + ((_b = codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.provider) === null || _b === void 0 ? void 0 : _b.slug) + "/" + (codeMapping === null || codeMapping === void 0 ? void 0 : codeMapping.integrationId) + "/?tab=userMappings", 'Configure User Mappings');
                        case 'missing_user_emails':
                            return errMessageComponent("The following emails do not have an Sentry user in the organization: " + organization.slug, values, "/settings/" + organization.slug + "/members/", 'Invite Users');
                        case 'teams_without_access':
                            return values.map(function (value) {
                                return errMessageComponent("The following team do not have access to the project: " + project.slug, [value], "/settings/" + organization.slug + "/teams/" + value.slice(1) + "/projects/", "Configure " + value + " Team Permissions");
                            });
                        default:
                            return null;
                    }
                };
                return (<alert_1.default key={id} type="error" icon={<icons_1.IconWarning size="md"/>} expand={Object.entries(errors)
                        .filter(function (_a) {
                        var _b = tslib_1.__read(_a, 2), _ = _b[0], values = _b[1];
                        return values.length;
                    })
                        .map(function (_a) {
                        var _b = tslib_1.__read(_a, 2), type = _b[0], values = _b[1];
                        return (<ErrorContainer key={id + "-" + type}>
                  {errMessage(type, values)}
                </ErrorContainer>);
                    })}>
            {"There were " + Object.values(errors).flat().length + " ownership issues within Sentry on the latest sync with the CODEOWNERS file"}
          </alert_1.default>);
            });
        };
        return _this;
    }
    ProjectOwnership.prototype.getTitle = function () {
        var project = this.props.project;
        return routeTitle_1.default(locale_1.t('Issue Owners'), project.slug, false);
    };
    ProjectOwnership.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var endpoints = [
            ['ownership', "/projects/" + organization.slug + "/" + project.slug + "/ownership/"],
            [
                'codeMappings',
                "/organizations/" + organization.slug + "/code-mappings/",
                { query: { projectId: project.id } },
            ],
            [
                'integrations',
                "/organizations/" + organization.slug + "/integrations/",
                { query: { features: ['codeowners'] } },
            ],
        ];
        if (organization.features.includes('integrations-codeowners')) {
            endpoints.push([
                'codeowners',
                "/projects/" + organization.slug + "/" + project.slug + "/codeowners/",
                { query: { expand: ['codeMapping', 'ownershipSyntax'] } },
            ]);
        }
        return endpoints;
    };
    ProjectOwnership.prototype.getPlaceholder = function () {
        return "#example usage\npath:src/example/pipeline/* person@sentry.io #infra\nurl:http://example.com/settings/* #product\ntags.sku_class:enterprise #enterprise";
    };
    ProjectOwnership.prototype.getDetail = function () {
        return locale_1.tct("Automatically assign issues and send alerts to the right people based on issue properties. [link:Learn more].", {
            link: (<externalLink_1.default href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
        });
    };
    ProjectOwnership.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, project = _a.project, organization = _a.organization;
        var _b = this.state, ownership = _b.ownership, codeowners = _b.codeowners;
        var disabled = !organization.access.includes('project:write');
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Issue Owners')} action={<react_1.Fragment>
              <button_1.default to={{
                    pathname: "/organizations/" + organization.slug + "/issues/",
                    query: { project: project.id },
                }} size="small">
                {locale_1.t('View Issues')}
              </button_1.default>
              <feature_1.default features={['integrations-codeowners']}>
                <CodeOwnerButton onClick={this.handleAddCodeOwner} size="small" priority="primary" data-test-id="add-codeowner-button">
                  {locale_1.t('Add Codeowner File')}
                </CodeOwnerButton>
              </feature_1.default>
            </react_1.Fragment>}/>
        <permissionAlert_1.default />
        {this.renderCodeOwnerErrors()}
        <rulesPanel_1.default data-test-id="issueowners-panel" type="issueowners" raw={ownership.raw || ''} dateUpdated={ownership.lastUpdated} placeholder={this.getPlaceholder()} detail={this.getDetail()} controls={[
                <button_1.default key="edit" size="small" onClick={function () {
                        return modal_1.openEditOwnershipRules({
                            organization: organization,
                            project: project,
                            ownership: ownership,
                            onSave: _this.handleOwnershipSave,
                        });
                    }} disabled={disabled}>
              {locale_1.t('Edit')}
            </button_1.default>,
            ]}/>
        <feature_1.default features={['integrations-codeowners']}>
          <codeowners_1.default codeowners={codeowners} onDelete={this.handleCodeownerDeleted} {...this.props}/>
        </feature_1.default>
        <form_1.default apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{
                fallthrough: ownership.fallthrough,
                autoAssignment: ownership.autoAssignment,
            }} hideFooter>
          <jsonForm_1.default forms={[
                {
                    title: locale_1.t('Issue Owners'),
                    fields: [
                        {
                            name: 'autoAssignment',
                            type: 'boolean',
                            label: locale_1.t('Automatically assign issues'),
                            help: locale_1.t('Assign issues when a new event matches the rules above.'),
                            disabled: disabled,
                        },
                        {
                            name: 'fallthrough',
                            type: 'boolean',
                            label: locale_1.t('Send alert to project members if there’s no assigned owner'),
                            help: locale_1.t('Alerts will be sent to all users who have access to this project.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </form_1.default>
      </react_1.Fragment>);
    };
    return ProjectOwnership;
}(asyncView_1.default));
exports.default = ProjectOwnership;
var CodeOwnerButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var ErrorContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-areas: 'message cta';\n  grid-template-columns: 2fr 1fr;\n  gap: ", ";\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-areas: 'message cta';\n  grid-template-columns: 2fr 1fr;\n  gap: ", ";\n  padding: ", " 0;\n"])), space_1.default(2), space_1.default(1.5));
var ErrorMessageContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-area: message;\n  display: grid;\n  gap: ", ";\n"], ["\n  grid-area: message;\n  display: grid;\n  gap: ", ";\n"])), space_1.default(1.5));
var ErrorCtaContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-area: cta;\n  justify-self: flex-end;\n  text-align: right;\n  line-height: 1.5;\n"], ["\n  grid-area: cta;\n  justify-self: flex-end;\n  text-align: right;\n  line-height: 1.5;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map