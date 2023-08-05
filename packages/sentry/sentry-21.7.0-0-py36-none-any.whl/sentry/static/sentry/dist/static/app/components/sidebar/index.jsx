Object.defineProperty(exports, "__esModule", { value: true });
exports.StyledSidebar = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var queryString = tslib_1.__importStar(require("query-string"));
var preferences_1 = require("app/actionCreators/preferences");
var sidebarPanelActions_1 = tslib_1.__importDefault(require("app/actions/sidebarPanelActions"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var preferencesStore_1 = tslib_1.__importDefault(require("app/stores/preferencesStore"));
var sidebarPanelStore_1 = tslib_1.__importDefault(require("app/stores/sidebarPanelStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var urls_1 = require("app/utils/discover/urls");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var broadcasts_1 = tslib_1.__importDefault(require("./broadcasts"));
var help_1 = tslib_1.__importDefault(require("./help"));
var onboardingStatus_1 = tslib_1.__importDefault(require("./onboardingStatus"));
var serviceIncidents_1 = tslib_1.__importDefault(require("./serviceIncidents"));
var sidebarDropdown_1 = tslib_1.__importDefault(require("./sidebarDropdown"));
var sidebarItem_1 = tslib_1.__importDefault(require("./sidebarItem"));
var types_1 = require("./types");
var SidebarOverride = hookOrDefault_1.default({
    hookName: 'sidebar:item-override',
    defaultComponent: function (_a) {
        var children = _a.children;
        return <React.Fragment>{children({})}</React.Fragment>;
    },
});
var Sidebar = /** @class */ (function (_super) {
    tslib_1.__extends(Sidebar, _super);
    function Sidebar(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            horizontal: false,
        };
        _this.mq = null;
        _this.sidebarRef = React.createRef();
        _this.toggleSidebar = function () {
            var collapsed = _this.props.collapsed;
            if (!collapsed) {
                preferences_1.hideSidebar();
            }
            else {
                preferences_1.showSidebar();
            }
        };
        _this.checkHash = function () {
            if (window.location.hash === '#welcome') {
                _this.togglePanel(types_1.SidebarPanelKey.OnboardingWizard);
            }
        };
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                horizontal: changed.matches,
            });
        };
        _this.togglePanel = function (panel) { return sidebarPanelActions_1.default.togglePanel(panel); };
        _this.hidePanel = function () { return sidebarPanelActions_1.default.hidePanel(); };
        // Keep the global selection querystring values in the path
        _this.navigateWithGlobalSelection = function (pathname, evt) {
            var _a;
            var globalSelectionRoutes = [
                'alerts',
                'alerts/rules',
                'dashboards',
                'issues',
                'releases',
                'user-feedback',
                'discover',
                'discover/results',
                'performance',
            ].map(function (route) { return "/organizations/" + _this.props.organization.slug + "/" + route + "/"; });
            // Only keep the querystring if the current route matches one of the above
            if (globalSelectionRoutes.includes(pathname)) {
                var query = utils_1.extractSelectionParameters((_a = _this.props.location) === null || _a === void 0 ? void 0 : _a.query);
                // Handle cmd-click (mac) and meta-click (linux)
                if (evt.metaKey) {
                    var q = queryString.stringify(query);
                    evt.currentTarget.href = evt.currentTarget.href + "?" + q;
                    return;
                }
                evt.preventDefault();
                react_router_1.browserHistory.push({ pathname: pathname, query: query });
            }
            _this.hidePanel();
        };
        if (!window.matchMedia) {
            return _this;
        }
        // TODO(billy): We should consider moving this into a component
        _this.mq = window.matchMedia("(max-width: " + theme_1.default.breakpoints[1] + ")");
        _this.mq.addListener(_this.handleMediaQueryChange);
        _this.state.horizontal = _this.mq.matches;
        return _this;
    }
    Sidebar.prototype.componentDidMount = function () {
        document.body.classList.add('body-sidebar');
        this.checkHash();
        this.doCollapse(this.props.collapsed);
    };
    // Sidebar doesn't use children, so don't use it to compare
    // Also ignore location, will re-render when routes change (instead of query params)
    //
    // NOTE(epurkhiser): The comment above is why I added `children?: never` as a
    // type to this component. I'm not sure the implications of removing this so
    // I've just left it for now.
    Sidebar.prototype.shouldComponentUpdate = function (_a, nextState) {
        var _children = _a.children, _location = _a.location, nextPropsToCompare = tslib_1.__rest(_a, ["children", "location"]);
        var _b = this.props, _childrenCurrent = _b.children, _locationCurrent = _b.location, currentPropsToCompare = tslib_1.__rest(_b, ["children", "location"]);
        return (!isEqual_1.default(currentPropsToCompare, nextPropsToCompare) ||
            !isEqual_1.default(this.state, nextState));
    };
    Sidebar.prototype.componentDidUpdate = function (prevProps) {
        var _a;
        var _b = this.props, collapsed = _b.collapsed, location = _b.location;
        // Close active panel if we navigated anywhere
        if ((location === null || location === void 0 ? void 0 : location.pathname) !== ((_a = prevProps.location) === null || _a === void 0 ? void 0 : _a.pathname)) {
            this.hidePanel();
        }
        // Collapse
        if (collapsed !== prevProps.collapsed) {
            this.doCollapse(collapsed);
        }
    };
    Sidebar.prototype.componentWillUnmount = function () {
        document.body.classList.remove('body-sidebar');
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
            this.mq = null;
        }
    };
    Sidebar.prototype.doCollapse = function (collapsed) {
        if (collapsed) {
            document.body.classList.add('collapsed');
        }
        else {
            document.body.classList.remove('collapsed');
        }
    };
    Sidebar.prototype.render = function () {
        var _this = this;
        var _a = this.props, activePanel = _a.activePanel, organization = _a.organization, collapsed = _a.collapsed;
        var horizontal = this.state.horizontal;
        var config = configStore_1.default.getConfig();
        var user = configStore_1.default.get('user');
        var hasPanel = !!activePanel;
        var orientation = horizontal ? 'top' : 'left';
        var sidebarItemProps = {
            orientation: orientation,
            collapsed: collapsed,
            hasPanel: hasPanel,
        };
        var hasOrganization = !!organization;
        var projects = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} index onClick={this.hidePanel} icon={<icons_1.IconProject size="md"/>} label={<guideAnchor_1.default target="projects">{locale_1.t('Projects')}</guideAnchor_1.default>} to={"/organizations/" + organization.slug + "/projects/"} id="projects"/>);
        var issues = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/issues/", evt);
            }} icon={<icons_1.IconIssues size="md"/>} label={<guideAnchor_1.default target="issues">{locale_1.t('Issues')}</guideAnchor_1.default>} to={"/organizations/" + organization.slug + "/issues/"} id="issues"/>);
        var discover2 = hasOrganization && (<feature_1.default hookName="feature-disabled:discover2-sidebar-item" features={['discover-basic']} organization={organization}>
        <sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection(urls_1.getDiscoverLandingUrl(organization), evt);
            }} icon={<icons_1.IconTelescope size="md"/>} label={<guideAnchor_1.default target="discover">{locale_1.t('Discover')}</guideAnchor_1.default>} to={urls_1.getDiscoverLandingUrl(organization)} id="discover-v2"/>
      </feature_1.default>);
        var performance = hasOrganization && (<feature_1.default hookName="feature-disabled:performance-sidebar-item" features={['performance-view']} organization={organization}>
        <SidebarOverride id="performance-override">
          {function (overideProps) { return (<sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                    return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/performance/", evt);
                }} icon={<icons_1.IconLightning size="md"/>} label={<guideAnchor_1.default target="performance">{locale_1.t('Performance')}</guideAnchor_1.default>} to={"/organizations/" + organization.slug + "/performance/"} id="performance" {...overideProps}/>); }}
        </SidebarOverride>
      </feature_1.default>);
        var releases = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/releases/", evt);
            }} icon={<icons_1.IconReleases size="md"/>} label={<guideAnchor_1.default target="releases">{locale_1.t('Releases')}</guideAnchor_1.default>} to={"/organizations/" + organization.slug + "/releases/"} id="releases"/>);
        var userFeedback = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/user-feedback/", evt);
            }} icon={<icons_1.IconSupport size="md"/>} label={locale_1.t('User Feedback')} to={"/organizations/" + organization.slug + "/user-feedback/"} id="user-feedback"/>);
        var alerts = hasOrganization && (<feature_1.default features={['incidents', 'alert-details-redesign']} requireAll={false}>
        {function (_a) {
                var features = _a.features;
                var hasIncidents = features.includes('incidents');
                var hasAlertList = features.includes('alert-details-redesign');
                var alertsPath = hasIncidents && !hasAlertList
                    ? "/organizations/" + organization.slug + "/alerts/"
                    : "/organizations/" + organization.slug + "/alerts/rules/";
                return (<sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) { return _this.navigateWithGlobalSelection(alertsPath, evt); }} icon={<icons_1.IconSiren size="md"/>} label={locale_1.t('Alerts')} to={alertsPath} id="alerts"/>);
            }}
      </feature_1.default>);
        var monitors = hasOrganization && (<feature_1.default features={['monitors']} organization={organization}>
        <sidebarItem_1.default {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/monitors/", evt);
            }} icon={<icons_1.IconLab size="md"/>} label={locale_1.t('Monitors')} to={"/organizations/" + organization.slug + "/monitors/"} id="monitors"/>
      </feature_1.default>);
        var dashboards = hasOrganization && (<feature_1.default hookName="feature-disabled:dashboards-sidebar-item" features={['discover', 'discover-query', 'dashboards-basic', 'dashboards-edit']} organization={organization} requireAll={false}>
        <sidebarItem_1.default {...sidebarItemProps} index onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/dashboards/", evt);
            }} icon={<icons_1.IconGraph size="md"/>} label={locale_1.t('Dashboards')} to={"/organizations/" + organization.slug + "/dashboards/"} id="customizable-dashboards" isNew/>
      </feature_1.default>);
        var activity = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconActivity size="md"/>} label={locale_1.t('Activity')} to={"/organizations/" + organization.slug + "/activity/"} id="activity"/>);
        var stats = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconStats size="md"/>} label={locale_1.t('Stats')} to={"/organizations/" + organization.slug + "/stats/"} id="stats"/>);
        var settings = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconSettings size="md"/>} label={locale_1.t('Settings')} to={"/settings/" + organization.slug + "/"} id="settings"/>);
        return (<exports.StyledSidebar ref={this.sidebarRef} collapsed={collapsed}>
        <SidebarSectionGroupPrimary>
          <SidebarSection>
            <sidebarDropdown_1.default orientation={orientation} collapsed={collapsed} org={organization} user={user} config={config}/>
          </SidebarSection>

          <PrimaryItems>
            {hasOrganization && (<React.Fragment>
                <SidebarSection>
                  {projects}
                  {issues}
                  {performance}
                  {releases}
                  {userFeedback}
                  {alerts}
                  {discover2}
                </SidebarSection>

                <SidebarSection>
                  {dashboards}
                  {monitors}
                </SidebarSection>

                <SidebarSection>
                  {activity}
                  {stats}
                </SidebarSection>

                <SidebarSection>{settings}</SidebarSection>
              </React.Fragment>)}
          </PrimaryItems>
        </SidebarSectionGroupPrimary>

        {hasOrganization && (<SidebarSectionGroup>
            <SidebarSection noMargin noPadding>
              <onboardingStatus_1.default org={organization} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(types_1.SidebarPanelKey.OnboardingWizard); }} hidePanel={this.hidePanel} {...sidebarItemProps}/>
            </SidebarSection>

            <SidebarSection>
              {hookStore_1.default.get('sidebar:bottom-items').length > 0 &&
                    hookStore_1.default.get('sidebar:bottom-items')[0](tslib_1.__assign({ organization: organization }, sidebarItemProps))}
              <help_1.default orientation={orientation} collapsed={collapsed} hidePanel={this.hidePanel} organization={organization}/>
              <broadcasts_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(types_1.SidebarPanelKey.Broadcasts); }} hidePanel={this.hidePanel} organization={organization}/>
              <serviceIncidents_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(types_1.SidebarPanelKey.StatusUpdate); }} hidePanel={this.hidePanel}/>
            </SidebarSection>

            {!horizontal && (<SidebarSection>
                <SidebarCollapseItem id="collapse" data-test-id="sidebar-collapse" {...sidebarItemProps} icon={<StyledIconChevron collapsed={collapsed}/>} label={collapsed ? locale_1.t('Expand') : locale_1.t('Collapse')} onClick={this.toggleSidebar}/>
              </SidebarSection>)}
          </SidebarSectionGroup>)}
      </exports.StyledSidebar>);
    };
    return Sidebar;
}(React.Component));
var SidebarContainer = /** @class */ (function (_super) {
    tslib_1.__extends(SidebarContainer, _super);
    function SidebarContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: preferencesStore_1.default.getInitialState().collapsed,
            activePanel: '',
        };
        _this.preferenceUnsubscribe = preferencesStore_1.default.listen(function (preferences) { return _this.onPreferenceChange(preferences); }, undefined);
        _this.sidebarUnsubscribe = sidebarPanelStore_1.default.listen(function (activePanel) { return _this.onSidebarPanelChange(activePanel); }, undefined);
        return _this;
    }
    SidebarContainer.prototype.componentWillUnmount = function () {
        this.preferenceUnsubscribe();
        this.sidebarUnsubscribe();
    };
    SidebarContainer.prototype.onPreferenceChange = function (preferences) {
        if (preferences.collapsed === this.state.collapsed) {
            return;
        }
        this.setState({ collapsed: preferences.collapsed });
    };
    SidebarContainer.prototype.onSidebarPanelChange = function (activePanel) {
        this.setState({ activePanel: activePanel });
    };
    SidebarContainer.prototype.render = function () {
        var _a = this.state, activePanel = _a.activePanel, collapsed = _a.collapsed;
        return <Sidebar {...this.props} {...{ activePanel: activePanel, collapsed: collapsed }}/>;
    };
    return SidebarContainer;
}(React.Component));
exports.default = withOrganization_1.default(SidebarContainer);
var responsiveFlex = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), theme_1.default.breakpoints[1]);
exports.StyledSidebar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  background: ", ";\n  color: ", ";\n  line-height: 1;\n  padding: 12px 0 2px; /* Allows for 32px avatars  */\n  width: ", ";\n  position: fixed;\n  top: ", ";\n  left: 0;\n  bottom: 0;\n  justify-content: space-between;\n  z-index: ", ";\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    top: 0;\n    left: 0;\n    right: 0;\n    height: ", ";\n    bottom: auto;\n    width: auto;\n    padding: 0 ", ";\n    align-items: center;\n  }\n"], ["\n  background: ", ";\n  background: ", ";\n  color: ", ";\n  line-height: 1;\n  padding: 12px 0 2px; /* Allows for 32px avatars  */\n  width: ", ";\n  position: fixed;\n  top: ", ";\n  left: 0;\n  bottom: 0;\n  justify-content: space-between;\n  z-index: ", ";\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    top: 0;\n    left: 0;\n    right: 0;\n    height: ", ";\n    bottom: auto;\n    width: auto;\n    padding: 0 ", ";\n    align-items: center;\n  }\n"])), function (p) { return p.theme.sidebar.background; }, function (p) { return p.theme.sidebarGradient; }, function (p) { return p.theme.sidebar.color; }, function (p) { return p.theme.sidebar.expandedWidth; }, function (p) { return (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0); }, function (p) { return p.theme.zIndex.sidebar; }, responsiveFlex, function (p) { return p.collapsed && "width: " + p.theme.sidebar.collapsedWidth + ";"; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.sidebar.mobileHeight; }, space_1.default(1));
var SidebarSectionGroup = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", ";\n  flex-shrink: 0; /* prevents shrinking on Safari */\n"], ["\n  ", ";\n  flex-shrink: 0; /* prevents shrinking on Safari */\n"])), responsiveFlex);
var SidebarSectionGroupPrimary = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", ";\n  /* necessary for child flexing on msedge and ff */\n  min-height: 0;\n  min-width: 0;\n  flex: 1;\n  /* expand to fill the entire height on mobile */\n  @media (max-width: ", ") {\n    height: 100%;\n    align-items: center;\n  }\n"], ["\n  ", ";\n  /* necessary for child flexing on msedge and ff */\n  min-height: 0;\n  min-width: 0;\n  flex: 1;\n  /* expand to fill the entire height on mobile */\n  @media (max-width: ", ") {\n    height: 100%;\n    align-items: center;\n  }\n"])), responsiveFlex, function (p) { return p.theme.breakpoints[1]; });
var PrimaryItems = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  overflow: auto;\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n  @media (max-height: 675px) and (min-width: ", ") {\n    border-bottom: 1px solid ", ";\n    padding-bottom: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;\n    &::-webkit-scrollbar {\n      background-color: transparent;\n      width: 8px;\n    }\n    &::-webkit-scrollbar-thumb {\n      background: ", ";\n      border-radius: 8px;\n    }\n  }\n  @media (max-width: ", ") {\n    overflow-y: visible;\n    flex-direction: row;\n    height: 100%;\n    align-items: center;\n    border-right: 1px solid ", ";\n    padding-right: ", ";\n    margin-right: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;\n    ::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"], ["\n  overflow: auto;\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n  @media (max-height: 675px) and (min-width: ", ") {\n    border-bottom: 1px solid ", ";\n    padding-bottom: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;\n    &::-webkit-scrollbar {\n      background-color: transparent;\n      width: 8px;\n    }\n    &::-webkit-scrollbar-thumb {\n      background: ", ";\n      border-radius: 8px;\n    }\n  }\n  @media (max-width: ", ") {\n    overflow-y: visible;\n    flex-direction: row;\n    height: 100%;\n    align-items: center;\n    border-right: 1px solid ", ";\n    padding-right: ", ";\n    margin-right: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;\n    ::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.gray400; }, space_1.default(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.gray400; }, space_1.default(1), space_1.default(0.5));
var SidebarSection = styled_1.default(SidebarSectionGroup)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    margin: 0;\n    padding: 0;\n  }\n\n  &:empty {\n    display: none;\n  }\n"], ["\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    margin: 0;\n    padding: 0;\n  }\n\n  &:empty {\n    display: none;\n  }\n"])), function (p) { return !p.noMargin && "margin: " + space_1.default(1) + " 0"; }, function (p) { return !p.noPadding && 'padding: 0 19px'; }, function (p) { return p.theme.breakpoints[0]; });
var ExpandedIcon = react_1.css(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  transition: 0.3s transform ease;\n  transform: rotate(270deg);\n"], ["\n  transition: 0.3s transform ease;\n  transform: rotate(270deg);\n"])));
var CollapsedIcon = react_1.css(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  transform: rotate(90deg);\n"], ["\n  transform: rotate(90deg);\n"])));
var StyledIconChevron = styled_1.default(function (_a) {
    var collapsed = _a.collapsed, props = tslib_1.__rest(_a, ["collapsed"]);
    return (<icons_1.IconChevron direction="left" size="md" isCircled css={[ExpandedIcon, collapsed && CollapsedIcon]} {...props}/>);
})(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject([""], [""])));
var SidebarCollapseItem = styled_1.default(sidebarItem_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=index.jsx.map