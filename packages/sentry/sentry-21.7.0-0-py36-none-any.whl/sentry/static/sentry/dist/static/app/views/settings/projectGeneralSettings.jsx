Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var projects_1 = require("app/actionCreators/projects");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var panels_1 = require("app/components/panels");
var projectGeneralSettings_1 = require("app/data/forms/projectGeneralSettings");
var locale_1 = require("app/locale");
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("app/utils/handleXhrErrorResponse"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var textField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var ProjectGeneralSettings = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectGeneralSettings, _super);
    function ProjectGeneralSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._form = {};
        _this.handleTransferFieldChange = function (id, value) {
            _this._form[id] = value;
        };
        _this.handleRemoveProject = function () {
            var orgId = _this.props.params.orgId;
            var project = _this.state.data;
            if (!project) {
                return;
            }
            projects_1.removeProject(_this.api, orgId, project).then(function () {
                // Need to hard reload because lots of components do not listen to Projects Store
                window.location.assign('/');
            }, handleXhrErrorResponse_1.default('Unable to remove project'));
        };
        _this.handleTransferProject = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var orgId, project, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        orgId = this.props.params.orgId;
                        project = this.state.data;
                        if (!project) {
                            return [2 /*return*/];
                        }
                        if (typeof this._form.email !== 'string' || this._form.email.length < 1) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.transferProject(this.api, orgId, project, this._form.email)];
                    case 2:
                        _a.sent();
                        // Need to hard reload because lots of components do not listen to Projects Store
                        window.location.assign('/');
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        if (err_1.status >= 500) {
                            handleXhrErrorResponse_1.default('Unable to transfer project')(err_1);
                        }
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.isProjectAdmin = function () { return new Set(_this.props.organization.access).has('project:admin'); };
        return _this;
    }
    ProjectGeneralSettings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Project Settings'), projectId, false);
    };
    ProjectGeneralSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['data', "/projects/" + orgId + "/" + projectId + "/"]];
    };
    ProjectGeneralSettings.prototype.renderRemoveProject = function () {
        var project = this.state.data;
        var isProjectAdmin = this.isProjectAdmin();
        var isInternal = project.isInternal;
        return (<field_1.default label={locale_1.t('Remove Project')} help={locale_1.tct('Remove the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                locale_1.t('You do not have the required permission to remove this project.')}

        {isInternal &&
                locale_1.t('This project cannot be removed. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<confirm_1.default onConfirm={this.handleRemoveProject} priority="danger" confirmText={locale_1.t('Remove project')} message={<div>
                <textBlock_1.default>
                  <strong>
                    {locale_1.t('Removing this project is permanent and cannot be undone!')}
                  </strong>
                </textBlock_1.default>
                <textBlock_1.default>
                  {locale_1.t('This will also remove all associated event data.')}
                </textBlock_1.default>
              </div>}>
            <div>
              <button_1.default className="ref-remove-project" type="button" priority="danger">
                {locale_1.t('Remove Project')}
              </button_1.default>
            </div>
          </confirm_1.default>)}
      </field_1.default>);
    };
    ProjectGeneralSettings.prototype.renderTransferProject = function () {
        var _this = this;
        var project = this.state.data;
        var isProjectAdmin = this.isProjectAdmin();
        var isInternal = project.isInternal;
        return (<field_1.default label={locale_1.t('Transfer Project')} help={locale_1.tct('Transfer the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                locale_1.t('You do not have the required permission to transfer this project.')}

        {isInternal &&
                locale_1.t('This project cannot be transferred. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<confirm_1.default onConfirm={this.handleTransferProject} priority="danger" confirmText={locale_1.t('Transfer project')} renderMessage={function (_a) {
                    var confirm = _a.confirm;
                    return (<div>
                <textBlock_1.default>
                  <strong>
                    {locale_1.t('Transferring this project is permanent and cannot be undone!')}
                  </strong>
                </textBlock_1.default>
                <textBlock_1.default>
                  {locale_1.t('Please enter the email of an organization owner to whom you would like to transfer this project.')}
                </textBlock_1.default>
                <panels_1.Panel>
                  <form_1.default hideFooter onFieldChange={_this.handleTransferFieldChange} onSubmit={function (_data, _onSuccess, _onError, e) {
                            e.stopPropagation();
                            confirm();
                        }}>
                    <textField_1.default name="email" label={locale_1.t('Organization Owner')} placeholder="admin@example.com" required help={locale_1.t('A request will be emailed to this address, asking the organization owner to accept the project transfer.')}/>
                  </form_1.default>
                </panels_1.Panel>
              </div>);
                }}>
            <div>
              <button_1.default className="ref-transfer-project" type="button" priority="danger">
                {locale_1.t('Transfer Project')}
              </button_1.default>
            </div>
          </confirm_1.default>)}
      </field_1.default>);
    };
    ProjectGeneralSettings.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var project = this.state.data;
        var _b = this.props.params, orgId = _b.orgId, projectId = _b.projectId;
        var endpoint = "/projects/" + orgId + "/" + projectId + "/";
        var access = new Set(organization.access);
        var jsonFormProps = {
            additionalFieldProps: {
                organization: organization,
            },
            features: new Set(organization.features),
            access: access,
            disabled: !access.has('project:write'),
        };
        var team = project.teams.length ? (_a = project.teams) === null || _a === void 0 ? void 0 : _a[0] : undefined;
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Project Settings')}/>
        <permissionAlert_1.default />

        <form_1.default saveOnBlur allowUndo initialData={tslib_1.__assign(tslib_1.__assign({}, project), { team: team })} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={function (resp) {
                _this.setState({ data: resp });
                if (projectId !== resp.slug) {
                    projects_1.changeProjectSlug(projectId, resp.slug);
                    // Container will redirect after stores get updated with new slug
                    _this.props.onChangeSlug(resp.slug);
                }
                // This will update our project context
                projectActions_1.default.updateSuccess(resp);
            }}>
          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Project Details')} fields={[projectGeneralSettings_1.fields.slug, projectGeneralSettings_1.fields.platform]}/>

          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Email')} fields={[projectGeneralSettings_1.fields.subjectPrefix]}/>

          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Event Settings')} fields={[projectGeneralSettings_1.fields.resolveAge]}/>

          <jsonForm_1.default {...jsonFormProps} title={locale_1.t('Client Security')} fields={[
                projectGeneralSettings_1.fields.allowedDomains,
                projectGeneralSettings_1.fields.scrapeJavaScript,
                projectGeneralSettings_1.fields.securityToken,
                projectGeneralSettings_1.fields.securityTokenHeader,
                projectGeneralSettings_1.fields.verifySSL,
            ]} renderHeader={function () { return (<panels_1.PanelAlert type="info">
                <textBlock_1.default noMargin>
                  {locale_1.tct('Configure origin URLs which Sentry should accept events from. This is used for communication with clients like [link].', {
                    link: (<a href="https://github.com/getsentry/sentry-javascript">
                          sentry-javascript
                        </a>),
                })}{' '}
                  {locale_1.tct('This will restrict requests based on the [Origin] and [Referer] headers.', {
                    Origin: <code>Origin</code>,
                    Referer: <code>Referer</code>,
                })}
                </textBlock_1.default>
              </panels_1.PanelAlert>); }}/>
        </form_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Project Administration')}</panels_1.PanelHeader>
          {this.renderRemoveProject()}
          {this.renderTransferProject()}
        </panels_1.Panel>
      </div>);
    };
    return ProjectGeneralSettings;
}(asyncView_1.default));
var ProjectGeneralSettingsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectGeneralSettingsContainer, _super);
    function ProjectGeneralSettingsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.changedSlug = undefined;
        _this.unsubscribe = projectsStore_1.default.listen(function () { return _this.onProjectsUpdate(); }, undefined);
        return _this;
    }
    ProjectGeneralSettingsContainer.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    ProjectGeneralSettingsContainer.prototype.onProjectsUpdate = function () {
        if (!this.changedSlug) {
            return;
        }
        var project = projectsStore_1.default.getBySlug(this.changedSlug);
        if (!project) {
            return;
        }
        react_router_1.browserHistory.replace(recreateRoute_1.default('', tslib_1.__assign(tslib_1.__assign({}, this.props), { params: tslib_1.__assign(tslib_1.__assign({}, this.props.params), { projectId: this.changedSlug }) })));
    };
    ProjectGeneralSettingsContainer.prototype.render = function () {
        var _this = this;
        return (<ProjectGeneralSettings onChangeSlug={function (newSlug) { return (_this.changedSlug = newSlug); }} {...this.props}/>);
    };
    return ProjectGeneralSettingsContainer;
}(react_1.Component));
exports.default = withOrganization_1.default(ProjectGeneralSettingsContainer);
//# sourceMappingURL=projectGeneralSettings.jsx.map