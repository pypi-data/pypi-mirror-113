Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var idBadge_1 = tslib_1.__importDefault(require("app/components/idBadge"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var organizationsStore_1 = tslib_1.__importDefault(require("app/stores/organizationsStore"));
var organizationStore_1 = tslib_1.__importDefault(require("app/stores/organizationStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var integrationIcon_1 = tslib_1.__importDefault(require("app/views/organizationIntegrations/integrationIcon"));
var selectStyles = {
    menu: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { position: 'auto', boxShadow: 'none', marginBottom: 0 })); },
    option: function (provided, state) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { opacity: state.isDisabled ? 0.6 : 1, cursor: state.isDisabled ? 'not-allowed' : 'pointer', pointerEvents: state.isDisabled ? 'none' : 'auto' })); },
};
var ContextPickerModal = /** @class */ (function (_super) {
    tslib_1.__extends(ContextPickerModal, _super);
    function ContextPickerModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // TODO(ts) The various generics in react-select types make getting this
        // right hard.
        _this.orgSelect = null;
        _this.projectSelect = null;
        _this.configSelect = null;
        // Performs checks to see if we need to prompt user
        // i.e. When there is only 1 org and no project is needed or
        // there is only 1 org and only 1 project (which should be rare)
        _this.navigateIfFinish = function (organizations, projects, latestOrg) {
            var _a;
            if (latestOrg === void 0) { latestOrg = _this.props.organization; }
            var _b = _this.props, needProject = _b.needProject, onFinish = _b.onFinish, nextPath = _b.nextPath, integrationConfigs = _b.integrationConfigs;
            var isSuperuser = (configStore_1.default.get('user') || {}).isSuperuser;
            // If no project is needed and theres only 1 org OR
            // if we need a project and there's only 1 project
            // then return because we can't navigate anywhere yet
            if ((!needProject && organizations.length !== 1) ||
                (needProject && projects.length !== 1) ||
                (integrationConfigs.length && isSuperuser)) {
                return;
            }
            // If there is only one org and we dont need a project slug, then call finish callback
            if (!needProject) {
                onFinish(replaceRouterParams_1.default(nextPath, {
                    orgId: organizations[0].slug,
                }));
                return;
            }
            // Use latest org or if only 1 org, use that
            var org = latestOrg;
            if (!org && organizations.length === 1) {
                org = organizations[0].slug;
            }
            onFinish(replaceRouterParams_1.default(nextPath, {
                orgId: org,
                projectId: projects[0].slug,
                project: (_a = _this.props.projects.find(function (p) { return p.slug === projects[0].slug; })) === null || _a === void 0 ? void 0 : _a.id,
            }));
        };
        _this.doFocus = function (ref) {
            if (!ref || _this.props.loading) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            var el = react_dom_1.default.findDOMNode(ref);
            if (el !== null) {
                var input = el.querySelector('input');
                input && input.focus();
            }
        };
        _this.handleSelectOrganization = function (_a) {
            var value = _a.value;
            // If we do not need to select a project, we can early return after selecting an org
            // No need to fetch org details
            if (!_this.props.needProject) {
                _this.navigateIfFinish([{ slug: value }], []);
                return;
            }
            _this.props.onSelectOrganization(value);
        };
        _this.handleSelectProject = function (_a) {
            var value = _a.value;
            var organization = _this.props.organization;
            if (!value || !organization) {
                return;
            }
            _this.navigateIfFinish([{ slug: organization }], [{ slug: value }]);
        };
        _this.handleSelectConfiguration = function (_a) {
            var value = _a.value;
            var _b = _this.props, onFinish = _b.onFinish, nextPath = _b.nextPath;
            if (!value) {
                return;
            }
            onFinish("" + nextPath + value + "/");
            return;
        };
        _this.getMemberProjects = function () {
            var projects = _this.props.projects;
            var nonMemberProjects = [];
            var memberProjects = [];
            projects.forEach(function (project) {
                return project.isMember ? memberProjects.push(project) : nonMemberProjects.push(project);
            });
            return [memberProjects, nonMemberProjects];
        };
        _this.onMenuOpen = function (ref, listItems, valueKey, currentSelected) {
            if (currentSelected === void 0) { currentSelected = ''; }
            // Hacky way to pre-focus to an item with newer versions of react select
            // See https://github.com/JedWatson/react-select/issues/3648
            setTimeout(function () {
                if (ref) {
                    var choices = ref.select.state.menuOptions.focusable;
                    var toBeFocused_1 = listItems.find(function (_a) {
                        var id = _a.id;
                        return id === currentSelected;
                    });
                    var selectedIndex = toBeFocused_1
                        ? choices.findIndex(function (option) { return option.value === toBeFocused_1[valueKey]; })
                        : 0;
                    if (selectedIndex >= 0 && toBeFocused_1) {
                        // Focusing selected option only if it exists
                        ref.select.scrollToFocusedOptionOnUpdate = true;
                        ref.select.inputIsHiddenAfterUpdate = false;
                        ref.select.setState({
                            focusedValue: null,
                            focusedOption: choices[selectedIndex],
                        });
                    }
                }
            });
        };
        // TODO(TS): Fix typings
        _this.customOptionProject = function (_a) {
            var label = _a.label, props = tslib_1.__rest(_a, ["label"]);
            var project = _this.props.projects.find(function (_a) {
                var slug = _a.slug;
                return props.value === slug;
            });
            if (!project) {
                return null;
            }
            return (<react_select_1.components.Option label={label} {...props}>
        <idBadge_1.default project={project} avatarSize={20} displayName={label} avatarProps={{ consistentWidth: true }}/>
      </react_select_1.components.Option>);
        };
        return _this;
    }
    ContextPickerModal.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, organizations = _a.organizations;
        // Don't make any assumptions if there are multiple organizations
        if (organizations.length !== 1) {
            return;
        }
        // If there is an org in context (and there's only 1 org available),
        // attempt to see if we need more info from user and redirect otherwise
        if (organization) {
            // This will handle if we can intelligently move the user forward
            this.navigateIfFinish([{ slug: organization }], projects);
            return;
        }
    };
    ContextPickerModal.prototype.componentDidUpdate = function (prevProps) {
        // Component may be mounted before projects is fetched, check if we can finish when
        // component is updated with projects
        if (JSON.stringify(prevProps.projects) !== JSON.stringify(this.props.projects)) {
            this.navigateIfFinish(this.props.organizations, this.props.projects);
        }
    };
    Object.defineProperty(ContextPickerModal.prototype, "headerText", {
        get: function () {
            var _a = this.props, needOrg = _a.needOrg, needProject = _a.needProject, integrationConfigs = _a.integrationConfigs;
            if (needOrg && needProject) {
                return locale_1.t('Select an organization and a project to continue');
            }
            if (needOrg) {
                return locale_1.t('Select an organization to continue');
            }
            if (needProject) {
                return locale_1.t('Select a project to continue');
            }
            if (integrationConfigs.length) {
                return locale_1.t('Select a configuration to continue');
            }
            // if neither project nor org needs to be selected, nothing will render anyways
            return '';
        },
        enumerable: false,
        configurable: true
    });
    ContextPickerModal.prototype.renderProjectSelectOrMessage = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects, comingFromProjectId = _a.comingFromProjectId;
        var _b = tslib_1.__read(this.getMemberProjects(), 2), memberProjects = _b[0], nonMemberProjects = _b[1];
        var isSuperuser = (configStore_1.default.get('user') || {}).isSuperuser;
        var projectOptions = [
            {
                label: locale_1.t('My Projects'),
                options: memberProjects.map(function (p) { return ({
                    value: p.slug,
                    label: locale_1.t("" + p.slug),
                    isDisabled: false,
                }); }),
            },
            {
                label: locale_1.t('All Projects'),
                options: nonMemberProjects.map(function (p) { return ({
                    value: p.slug,
                    label: locale_1.t("" + p.slug),
                    isDisabled: isSuperuser ? false : true,
                }); }),
            },
        ];
        if (!projects.length) {
            return (<div>
          {locale_1.tct('You have no projects. Click [link] to make one.', {
                    link: (<link_1.default to={"/organizations/" + organization + "/projects/new/"}>{locale_1.t('here')}</link_1.default>),
                })}
        </div>);
        }
        return (<StyledSelectControl ref={function (ref) {
                _this.projectSelect = ref;
                _this.doFocus(_this.projectSelect);
            }} placeholder={locale_1.t('Select a Project to continue')} name="project" options={projectOptions} onChange={this.handleSelectProject} onMenuOpen={function () {
                return _this.onMenuOpen(_this.projectSelect, projects, 'slug', comingFromProjectId);
            }} components={{ Option: this.customOptionProject, DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>);
    };
    ContextPickerModal.prototype.renderIntegrationConfigs = function () {
        var _this = this;
        var integrationConfigs = this.props.integrationConfigs;
        var isSuperuser = (configStore_1.default.get('user') || {}).isSuperuser;
        var options = [
            {
                label: locale_1.tct('[providerName] Configurations', {
                    providerName: integrationConfigs[0].provider.name,
                }),
                options: integrationConfigs.map(function (config) { return ({
                    value: config.id,
                    label: (<StyledIntegrationItem>
              <integrationIcon_1.default size={22} integration={config}/>
              <span>{config.domainName}</span>
            </StyledIntegrationItem>),
                    isDisabled: isSuperuser ? false : true,
                }); }),
            },
        ];
        return (<StyledSelectControl ref={function (ref) {
                _this.configSelect = ref;
                _this.doFocus(_this.configSelect);
            }} placeholder={locale_1.t('Select a configuration to continue')} name="configurations" options={options} onChange={this.handleSelectConfiguration} onMenuOpen={function () { return _this.onMenuOpen(_this.configSelect, integrationConfigs, 'id'); }} components={{ DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>);
    };
    ContextPickerModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, needOrg = _a.needOrg, needProject = _a.needProject, organization = _a.organization, organizations = _a.organizations, loading = _a.loading, Header = _a.Header, Body = _a.Body, integrationConfigs = _a.integrationConfigs;
        var isSuperuser = (configStore_1.default.get('user') || {}).isSuperuser;
        var shouldShowProjectSelector = organization && needProject && !loading;
        var shouldShowConfigSelector = integrationConfigs.length > 0 && isSuperuser;
        var orgChoices = organizations
            .filter(function (_a) {
            var status = _a.status;
            return status.id !== 'pending_deletion';
        })
            .map(function (_a) {
            var slug = _a.slug;
            return ({ label: slug, value: slug });
        });
        var shouldShowPicker = needOrg || needProject || shouldShowConfigSelector;
        if (!shouldShowPicker) {
            return null;
        }
        return (<react_1.Fragment>
        <Header closeButton>{this.headerText}</Header>
        <Body>
          {loading && <StyledLoadingIndicator overlay/>}
          {needOrg && (<StyledSelectControl ref={function (ref) {
                    _this.orgSelect = ref;
                    if (shouldShowProjectSelector) {
                        return;
                    }
                    _this.doFocus(_this.orgSelect);
                }} placeholder={locale_1.t('Select an Organization')} name="organization" options={orgChoices} value={organization} onChange={this.handleSelectOrganization} components={{ DropdownIndicator: null }} styles={selectStyles} menuIsOpen/>)}

          {shouldShowProjectSelector && this.renderProjectSelectOrMessage()}
          {shouldShowConfigSelector && this.renderIntegrationConfigs()}
        </Body>
      </react_1.Fragment>);
    };
    return ContextPickerModal;
}(react_1.Component));
var ContextPickerModalContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ContextPickerModalContainer, _super);
    function ContextPickerModalContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.unlistener = organizationsStore_1.default.listen(function (organizations) { return _this.setState({ organizations: organizations }); }, undefined);
        _this.handleSelectOrganization = function (organizationSlug) {
            _this.setState({ selectedOrganization: organizationSlug });
        };
        return _this;
    }
    ContextPickerModalContainer.prototype.getDefaultState = function () {
        var _a;
        var storeState = organizationStore_1.default.get();
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { organizations: organizationsStore_1.default.getAll(), selectedOrganization: (_a = storeState.organization) === null || _a === void 0 ? void 0 : _a.slug });
    };
    ContextPickerModalContainer.prototype.getEndpoints = function () {
        var configUrl = this.props.configUrl;
        if (configUrl) {
            return [['integrationConfigs', configUrl]];
        }
        return [];
    };
    ContextPickerModalContainer.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    ContextPickerModalContainer.prototype.renderModal = function (_a) {
        var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, integrationConfigs = _a.integrationConfigs;
        return (<ContextPickerModal {...this.props} projects={projects || []} loading={!initiallyLoaded} organizations={this.state.organizations} organization={this.state.selectedOrganization} onSelectOrganization={this.handleSelectOrganization} integrationConfigs={integrationConfigs || []}/>);
    };
    ContextPickerModalContainer.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, projectSlugs = _b.projectSlugs, configUrl = _b.configUrl;
        if (configUrl && this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        if ((_a = this.state.integrationConfigs) === null || _a === void 0 ? void 0 : _a.length) {
            return this.renderModal({
                integrationConfigs: this.state.integrationConfigs,
                initiallyLoaded: !this.state.loading,
            });
        }
        if (this.state.selectedOrganization) {
            return (<projects_1.default orgId={this.state.selectedOrganization} allProjects={!(projectSlugs === null || projectSlugs === void 0 ? void 0 : projectSlugs.length)} slugs={projectSlugs}>
          {function (_a) {
                    var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded;
                    return _this.renderModal({ projects: projects, initiallyLoaded: initiallyLoaded });
                }}
        </projects_1.default>);
        }
        return this.renderModal({});
    };
    return ContextPickerModalContainer;
}(asyncComponent_1.default));
exports.default = ContextPickerModalContainer;
var StyledSelectControl = styled_1.default(selectControl_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(1));
var StyledLoadingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  z-index: 1;\n"], ["\n  z-index: 1;\n"])));
var StyledIntegrationItem = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", " auto;\n  grid-template-rows: 1fr;\n"], ["\n  display: grid;\n  grid-template-columns: ", " auto;\n  grid-template-rows: 1fr;\n"])), space_1.default(4));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=contextPickerModal.jsx.map