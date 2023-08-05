Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationContext = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var modal_1 = require("app/actionCreators/modal");
var organization_1 = require("app/actionCreators/organization");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var sidebar_1 = tslib_1.__importDefault(require("app/components/sidebar"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var organizationStore_1 = tslib_1.__importDefault(require("app/stores/organizationStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var callIfFunction_1 = require("app/utils/callIfFunction");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var defaultProps = {
    detailed: true,
};
var OrganizationContext = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationContext, _super);
    function OrganizationContext(props) {
        var _this = _super.call(this, props) || this;
        _this.unlisteners = [
            projectActions_1.default.createSuccess.listen(function () { return _this.onProjectCreation(); }, undefined),
            organizationStore_1.default.listen(function (data) { return _this.loadOrganization(data); }, undefined),
        ];
        _this.remountComponent = function () {
            _this.setState(OrganizationContext.getDefaultState(_this.props), _this.fetchData);
        };
        _this.state = OrganizationContext.getDefaultState(props);
        return _this;
    }
    OrganizationContext.getDerivedStateFromProps = function (props, prevState) {
        var prevProps = prevState.prevProps;
        if (OrganizationContext.shouldRemount(prevProps, props)) {
            return OrganizationContext.getDefaultState(props);
        }
        var organizationsLoading = props.organizationsLoading, location = props.location, params = props.params;
        var orgId = params.orgId;
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { prevProps: {
                orgId: orgId,
                organizationsLoading: organizationsLoading,
                location: location,
            } });
    };
    OrganizationContext.shouldRemount = function (prevProps, props) {
        var hasOrgIdAndChanged = prevProps.orgId && props.params.orgId && prevProps.orgId !== props.params.orgId;
        var hasOrgId = props.params.orgId ||
            (props.useLastOrganization && configStore_1.default.get('lastOrganization'));
        // protect against the case where we finish fetching org details
        // and then `OrganizationsStore` finishes loading:
        // only fetch in the case where we don't have an orgId
        //
        // Compare `getOrganizationSlug`  because we may have a last used org from server
        // if there is no orgId in the URL
        var organizationLoadingChanged = prevProps.organizationsLoading !== props.organizationsLoading &&
            props.organizationsLoading === false;
        return (hasOrgIdAndChanged ||
            (!hasOrgId && organizationLoadingChanged) ||
            (props.location.state === 'refresh' && prevProps.location.state !== 'refresh'));
    };
    OrganizationContext.getDefaultState = function (props) {
        var prevProps = {
            orgId: props.params.orgId,
            organizationsLoading: props.organizationsLoading,
            location: props.location,
        };
        if (OrganizationContext.isOrgStorePopulatedCorrectly(props)) {
            // retrieve initial state from store
            return tslib_1.__assign(tslib_1.__assign({}, organizationStore_1.default.get()), { prevProps: prevProps });
        }
        return {
            loading: true,
            error: null,
            errorType: null,
            organization: null,
            prevProps: prevProps,
        };
    };
    OrganizationContext.getOrganizationSlug = function (props) {
        var _a, _b;
        return (props.params.orgId ||
            (props.useLastOrganization &&
                (configStore_1.default.get('lastOrganization') ||
                    ((_b = (_a = props.organizations) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.slug))));
    };
    OrganizationContext.isOrgChanging = function (props) {
        var organization = organizationStore_1.default.get().organization;
        if (!organization) {
            return false;
        }
        return organization.slug !== OrganizationContext.getOrganizationSlug(props);
    };
    OrganizationContext.isOrgStorePopulatedCorrectly = function (props) {
        var detailed = props.detailed;
        var _a = organizationStore_1.default.get(), organization = _a.organization, dirty = _a.dirty;
        return (!dirty &&
            organization &&
            !OrganizationContext.isOrgChanging(props) &&
            (!detailed || (detailed && organization.projects && organization.teams)));
    };
    OrganizationContext.prototype.getChildContext = function () {
        return {
            organization: this.state.organization,
        };
    };
    OrganizationContext.prototype.componentDidMount = function () {
        this.fetchData(true);
    };
    OrganizationContext.prototype.componentDidUpdate = function (prevProps) {
        var remountPrevProps = {
            orgId: prevProps.params.orgId,
            organizationsLoading: prevProps.organizationsLoading,
            location: prevProps.location,
        };
        if (OrganizationContext.shouldRemount(remountPrevProps, this.props)) {
            this.remountComponent();
        }
    };
    OrganizationContext.prototype.componentWillUnmount = function () {
        this.unlisteners.forEach(callIfFunction_1.callIfFunction);
    };
    OrganizationContext.prototype.onProjectCreation = function () {
        // If a new project was created, we need to re-fetch the
        // org details endpoint, which will propagate re-rendering
        // for the entire component tree
        organization_1.fetchOrganizationDetails(this.props.api, OrganizationContext.getOrganizationSlug(this.props), true, true);
    };
    OrganizationContext.prototype.isLoading = function () {
        // In the absence of an organization slug, the loading state should be
        // derived from this.props.organizationsLoading from OrganizationsStore
        if (!OrganizationContext.getOrganizationSlug(this.props)) {
            return this.props.organizationsLoading;
        }
        // The following loading logic exists because we could either be waiting for
        // the whole organization object to come in or just the teams and projects.
        var _a = this.state, loading = _a.loading, error = _a.error, organization = _a.organization;
        var detailed = this.props.detailed;
        return (loading ||
            (!error &&
                detailed &&
                (!organization || !organization.projects || !organization.teams)));
    };
    OrganizationContext.prototype.fetchData = function (isInitialFetch) {
        if (isInitialFetch === void 0) { isInitialFetch = false; }
        if (!OrganizationContext.getOrganizationSlug(this.props)) {
            return;
        }
        // fetch from the store, then fetch from the API if necessary
        if (OrganizationContext.isOrgStorePopulatedCorrectly(this.props)) {
            return;
        }
        analytics_1.metric.mark({ name: 'organization-details-fetch-start' });
        organization_1.fetchOrganizationDetails(this.props.api, OrganizationContext.getOrganizationSlug(this.props), this.props.detailed, !OrganizationContext.isOrgChanging(this.props), // if true, will preserve a lightweight org that was fetched,
        isInitialFetch);
    };
    OrganizationContext.prototype.loadOrganization = function (orgData) {
        var _this = this;
        var organization = orgData.organization, error = orgData.error;
        var hooks = [];
        if (organization && !error) {
            hookStore_1.default.get('organization:header').forEach(function (cb) {
                hooks.push(cb(organization));
            });
            // Configure scope to have organization tag
            Sentry.configureScope(function (scope) {
                // XXX(dcramer): this is duplicated in sdk.py on the backend
                scope.setTag('organization', organization.id);
                scope.setTag('organization.slug', organization.slug);
                scope.setContext('organization', { id: organization.id, slug: organization.slug });
            });
        }
        else if (error) {
            // If user is superuser, open sudo window
            var user = configStore_1.default.get('user');
            if (!user || !user.isSuperuser || error.status !== 403) {
                // This `catch` can swallow up errors in development (and tests)
                // So let's log them. This may create some noise, especially the test case where
                // we specifically test this branch
                console.error(error); // eslint-disable-line no-console
            }
            else {
                modal_1.openSudo({
                    retryRequest: function () { return Promise.resolve(_this.fetchData()); },
                });
            }
        }
        this.setState(tslib_1.__assign(tslib_1.__assign({}, orgData), { hooks: hooks }), function () {
            // Take a measurement for when organization details are done loading and the new state is applied
            if (organization) {
                analytics_1.metric.measure({
                    name: 'app.component.perf',
                    start: 'organization-details-fetch-start',
                    data: {
                        name: 'org-details',
                        route: getRouteStringFromRoutes_1.default(_this.props.routes),
                        organization_id: parseInt(organization.id, 10),
                    },
                });
            }
        });
    };
    OrganizationContext.prototype.getOrganizationDetailsEndpoint = function () {
        return "/organizations/" + OrganizationContext.getOrganizationSlug(this.props) + "/";
    };
    OrganizationContext.prototype.getTitle = function () {
        if (this.state.organization) {
            return this.state.organization.name;
        }
        return 'Sentry';
    };
    OrganizationContext.prototype.renderSidebar = function () {
        if (!this.props.includeSidebar) {
            return null;
        }
        var _a = this.props, _ = _a.children, props = tslib_1.__rest(_a, ["children"]);
        return <sidebar_1.default {...props} organization={this.state.organization}/>;
    };
    OrganizationContext.prototype.renderError = function () {
        var errorComponent;
        switch (this.state.errorType) {
            case constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS:
                // We can still render when an org can't be loaded due to 401. The
                // backend will handle redirects when this is a problem.
                return this.renderBody();
            case constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND:
                errorComponent = (<alert_1.default type="error">
            {locale_1.t('The organization you were looking for was not found.')}
          </alert_1.default>);
                break;
            default:
                errorComponent = <loadingError_1.default onRetry={this.remountComponent}/>;
        }
        return <ErrorWrapper>{errorComponent}</ErrorWrapper>;
    };
    OrganizationContext.prototype.renderBody = function () {
        return (<react_document_title_1.default title={this.getTitle()}>
        <div className="app">
          {this.state.hooks}
          {this.renderSidebar()}
          {this.props.children}
        </div>
      </react_document_title_1.default>);
    };
    OrganizationContext.prototype.render = function () {
        if (this.isLoading()) {
            return (<loadingIndicator_1.default triangle>
          {locale_1.t('Loading data for your organization.')}
        </loadingIndicator_1.default>);
        }
        if (this.state.error) {
            return (<React.Fragment>
          {this.renderSidebar()}
          {this.renderError()}
        </React.Fragment>);
        }
        return this.renderBody();
    };
    OrganizationContext.childContextTypes = {
        organization: sentryTypes_1.default.Organization,
    };
    OrganizationContext.defaultProps = defaultProps;
    return OrganizationContext;
}(React.Component));
exports.OrganizationContext = OrganizationContext;
exports.default = withApi_1.default(withOrganizations_1.default(Sentry.withProfiler(OrganizationContext)));
var ErrorWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(3));
var templateObject_1;
//# sourceMappingURL=organizationContext.jsx.map