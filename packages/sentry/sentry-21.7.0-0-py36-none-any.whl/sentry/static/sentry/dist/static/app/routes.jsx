Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var lazyLoad_1 = tslib_1.__importDefault(require("app/components/lazyLoad"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var errorHandler_1 = tslib_1.__importDefault(require("app/utils/errorHandler"));
var app_1 = tslib_1.__importDefault(require("app/views/app"));
var layout_1 = tslib_1.__importDefault(require("app/views/auth/layout"));
var container_1 = tslib_1.__importDefault(require("app/views/issueList/container"));
var overview_1 = tslib_1.__importDefault(require("app/views/issueList/overview"));
var organizationContext_1 = tslib_1.__importDefault(require("app/views/organizationContext"));
var organizationDetails_1 = tslib_1.__importStar(require("app/views/organizationDetails"));
var header_1 = require("app/views/organizationGroupDetails/header");
var organizationRoot_1 = tslib_1.__importDefault(require("app/views/organizationRoot"));
var projectEventRedirect_1 = tslib_1.__importDefault(require("app/views/projectEventRedirect"));
var redirectDeprecatedProjectRoute_1 = tslib_1.__importDefault(require("app/views/projects/redirectDeprecatedProjectRoute"));
var routeNotFound_1 = tslib_1.__importDefault(require("app/views/routeNotFound"));
var settingsProjectProvider_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsProjectProvider"));
var settingsWrapper_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsWrapper"));
var appendTrailingSlash = function (nextState, replace) {
    var lastChar = nextState.location.pathname.slice(-1);
    if (lastChar !== '/') {
        replace(nextState.location.pathname + '/');
    }
};
/**
 * We add some additional props to our routes
 */
var Route = react_router_1.Route;
var IndexRoute = react_router_1.IndexRoute;
/**
 * Use react-router to lazy load a route. Use this for codesplitting containers (e.g. SettingsLayout)
 *
 * The method for lazy loading a route leaf node is using the <LazyLoad> component + `componentPromise`.
 * The reason for this is because react-router handles the route tree better and if we use <LazyLoad> it will end
 * up having to re-render more components than necessary.
 */
var lazyLoad = function (cb) { return function (m) { return cb(null, m.default); }; };
var hook = function (name) { return hookStore_1.default.get(name).map(function (cb) { return cb(); }); };
function routes() {
    var accountSettingsRoutes = (<React.Fragment>
      <react_router_1.IndexRedirect to="details/"/>

      <Route path="details/" name="Details" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="notifications/" name="Notifications">
        <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountNotifications')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path=":fineTuneType/" name="Fine Tune Alerts" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountNotificationFineTuning')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route path="emails/" name="Emails" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountEmails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="authorizations/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountAuthorizations')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route name="Security" path="security/">
        <Route componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSecurity/accountSecurityWrapper')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}>
          <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSecurity')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="session-history/" name="Session History" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSecurity/sessionHistory')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="mfa/:authId/" name="Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSecurity/accountSecurityDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>

        <Route path="mfa/:authId/enroll/" name="Enroll" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSecurity/accountSecurityEnroll')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <Route path="subscriptions/" name="Subscriptions" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSubscriptions')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="identities/" name="Identities" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountIdentities')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="api/" name="API">
        <react_router_1.IndexRedirect to="auth-tokens/"/>

        <Route path="auth-tokens/" name="Auth Tokens">
          <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/apiTokens')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="new-token/" name="Create New Token" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/apiNewToken')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>

        <Route path="applications/" name="Applications">
          <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/apiApplications')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path=":appId/" name="Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/apiApplications/details')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>

        {hook('routes:api')}
      </Route>

      <Route path="close-account/" name="Close Account" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountClose')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
    </React.Fragment>);
    var projectSettingsRoutes = (<React.Fragment>
      <IndexRoute name="General" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectGeneralSettings')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="teams/" name="Teams" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectTeams')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route name="Alerts" path="alerts/" component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectAlerts')); }); }}>
        <IndexRoute component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectAlerts/settings')); }); }}/>
        <react_router_1.Redirect from="new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/" to="/organizations/:orgId/alerts/rules/"/>
        <react_router_1.Redirect from="rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="metric-rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/:ruleId/" to="/organizations/:orgId/alerts/rules/:projectId/:ruleId/"/>
        <react_router_1.Redirect from="metric-rules/:ruleId/" to="/organizations/:orgId/alerts/metric-rules/:projectId/:ruleId/"/>
      </Route>

      <Route name="Environments" path="environments/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectEnvironments')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
        <IndexRoute />
        <Route path="hidden/"/>
      </Route>
      <Route name="Tags" path="tags/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectTags')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/:projectId/plugins/"/>
      <Route path="release-tracking/" name="Release Tracking" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectReleaseTracking')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="ownership/" name="Issue Owners" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectOwnership')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="data-forwarding/" name="Data Forwarding" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectDataForwarding')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route name={locale_1.t('Security & Privacy')} path="security-and-privacy/" component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSecurityAndPrivacy')); }); }}/>
      <Route path="debug-symbols/" name="Debug Information Files" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectDebugFiles')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="proguard/" name={locale_1.t('ProGuard Mappings')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectProguard')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="performance/" name={locale_1.t('Performance')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectPerformance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="source-maps/" name={locale_1.t('Source Maps')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSourceMaps')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSourceMaps/list')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path=":name/" name={locale_1.t('Archive')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSourceMaps/detail')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route path="processing-issues/" name="Processing Issues" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectProcessingIssues')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="filters/" name="Inbound Filters" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectFilters')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
        <react_router_1.IndexRedirect to="data-filters/"/>
        <Route path=":filterType/"/>
      </Route>
      <Route name={locale_1.t('Filters & Sampling')} path="filters-and-sampling/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/filtersAndSampling')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="issue-grouping/" name={locale_1.t('Issue Grouping')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectIssueGrouping')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="hooks/" name="Service Hooks" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectServiceHooks')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="hooks/new/" name="Create Service Hook" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectCreateServiceHook')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="hooks/:hookId/" name="Service Hook Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectServiceHookDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <Route path="keys/" name="Client Keys">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectKeys/list')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path=":keyId/" name="Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectKeys/details')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route path="user-feedback/" name="User Feedback" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectUserFeedback')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      <react_router_1.Redirect from="csp/" to="security-headers/"/>
      <Route path="security-headers/" name="Security Headers">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSecurityHeaders')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path="csp/" name="Content Security Policy" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSecurityHeaders/csp')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path="expect-ct/" name="Certificate Transparency" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSecurityHeaders/expectCt')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path="hpkp/" name="HPKP" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectSecurityHeaders/hpkp')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route path="plugins/" name="Legacy Integrations">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectPlugins')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path=":pluginId/" name="Integration Details" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/projectPlugins/details')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route path="install/" name="Configuration">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/overview')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path=":platform/" name="Docs" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/platformOrIntegration')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
    </React.Fragment>);
    // This is declared in the routes() function because some routes need the
    // hook store which is not available at import time.
    var orgSettingsRoutes = (<React.Fragment>
      <IndexRoute name="General" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationGeneralSettings')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="projects/" name="Projects" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationProjects')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="api-keys/" name="API Key">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationApiKeys')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path=":apiKey/" name="Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationApiKeys/organizationApiKeyDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <Route path="audit-log/" name="Audit Log" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationAuditLog')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="auth/" name="Auth Providers" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationAuth')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="members/" name="Members">
        <Route componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationMembers/organizationMembersWrapper')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}>
          <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationMembers/organizationMembersList')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>

          <Route path="requests/" name="Requests" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationMembers/organizationRequestsView')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>

        <Route path=":memberId/" name="Details" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationMembers/organizationMemberDetail')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <Route path="rate-limits/" name="Rate Limits" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationRateLimits')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route name={locale_1.t('Relay')} path="relay/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationRelay')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="repos/" name="Repositories" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationRepositories')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="performance/" name={locale_1.t('Performance')} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationPerformance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route path="settings/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationGeneralSettings')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route name={locale_1.t('Security & Privacy')} path="security-and-privacy/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationSecurityAndPrivacy')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>

      <Route name="Teams" path="teams/">
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationTeams')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route name="Team" path=":teamId/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationTeams/teamDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}>
          <react_router_1.IndexRedirect to="members/"/>
          <Route path="members/" name="Members" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationTeams/teamMembers')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="projects/" name="Projects" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationTeams/teamProjects')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="settings/" name="settings" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationTeams/teamSettings')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>
      </Route>

      <react_router_1.Redirect from="plugins/" to="integrations/"/>
      <Route name="Integrations" path="plugins/">
        <Route name="Integration Details" path=":integrationSlug/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationIntegrations/pluginDetailedView')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <react_router_1.Redirect from="sentry-apps/" to="integrations/"/>
      <Route name="Integrations" path="sentry-apps/">
        <Route name="Details" path=":integrationSlug" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationIntegrations/sentryAppDetailedView')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <react_router_1.Redirect from="document-integrations/" to="integrations/"/>
      <Route name="Integrations" path="document-integrations/">
        <Route name="Details" path=":integrationSlug" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationIntegrations/docIntegrationDetailedView')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
      <Route name="Integrations" path="integrations/">
        <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationIntegrations/integrationListDirectory')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="Integration Details" path=":integrationSlug" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationIntegrations/integrationDetailedView')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="Configure Integration" path=":providerKey/:integrationId/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationIntegrations/configureIntegration')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>

      <Route name="Developer Settings" path="developer-settings/">
        <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationDeveloperSettings')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="New Public Integration" path="new-public/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="New Internal Integration" path="new-internal/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="Edit Integration" path=":appSlug/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route name="Integration Dashboard" path=":appSlug/dashboard/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDashboard')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
      </Route>
    </React.Fragment>);
    return (<Route>
      {constants_1.EXPERIMENTAL_SPA && (<Route path="/auth/login/" component={errorHandler_1.default(layout_1.default)}>
          <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/auth/login')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>)}

      <Route path="/" component={errorHandler_1.default(app_1.default)}>
        <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/app/root')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/accept/:memberId/:token/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/acceptOrganizationInvite')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path="/accept-transfer/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/acceptProjectTransfer')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <Route path="/extensions/external-install/:integrationSlug/:installationId" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/integrationOrganizationLink')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/extensions/:integrationSlug/link/" getComponent={function (_loc, cb) {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/integrationOrganizationLink')); }).then(lazyLoad(cb));
        }}/>

        <Route path="/sentry-apps/:sentryAppSlug/external-install/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/sentryAppExternalInstallation')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        <react_router_1.Redirect from="/account/" to="/settings/account/details/"/>

        <react_router_1.Redirect from="/share/group/:shareId/" to="/share/issue/:shareId/"/>
        <Route path="/share/issue/:shareId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/sharedGroupDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/organizations/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationCreate')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/organizations/:orgId/data-export/:dataExportId" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dataExport/dataDownload')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/organizations/:orgId/disabled-member/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/disabledMember')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/join-request/:orgId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationJoinRequest')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

        <Route path="/onboarding/:orgId/" component={errorHandler_1.default(organizationContext_1.default)}>
          <react_router_1.IndexRedirect to="welcome/"/>
          <Route path=":step/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/onboarding/onboarding')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
        </Route>

        {/* Settings routes */}
        <Route component={errorHandler_1.default(organizationDetails_1.default)}>
          <Route path="/settings/" name="Settings" component={settingsWrapper_1.default}>
            <IndexRoute getComponent={function (_loc, cb) {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/settingsIndex')); }).then(lazyLoad(cb));
        }}/>

            <Route path="account/" name="Account" getComponent={function (_loc, cb) {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/account/accountSettingsLayout')); }).then(lazyLoad(cb));
        }}>
              {accountSettingsRoutes}
            </Route>

            <Route name="Organization" path=":orgId/">
              <Route getComponent={function (_loc, cb) {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/organization/organizationSettingsLayout')); }).then(lazyLoad(cb));
        }}>
                {hook('routes:organization')}
                {orgSettingsRoutes}
              </Route>

              <Route name="Project" path="projects/:projectId/" getComponent={function (_loc, cb) {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/settings/project/projectSettingsLayout')); }).then(lazyLoad(cb));
        }}>
                <Route component={errorHandler_1.default(settingsProjectProvider_1.default)}>
                  {projectSettingsRoutes}
                </Route>
              </Route>

              <react_router_1.Redirect from=":projectId/" to="projects/:projectId/"/>
              <react_router_1.Redirect from=":projectId/alerts/" to="projects/:projectId/alerts/"/>
              <react_router_1.Redirect from=":projectId/alerts/rules/" to="projects/:projectId/alerts/rules/"/>
              <react_router_1.Redirect from=":projectId/alerts/rules/:ruleId/" to="projects/:projectId/alerts/rules/:ruleId/"/>
            </Route>
          </Route>
        </Route>

        {/* A route tree for lightweight organizational detail views. We place
      this above the heavyweight organization detail views because there
      exist some redirects from deprecated routes which should not take
      precedence over these lightweight routes */}
        <Route component={errorHandler_1.default(organizationDetails_1.LightWeightOrganizationDetails)}>
          <Route path="/organizations/:orgId/projects/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectsDashboard')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          <Route path="/organizations/:orgId/dashboards/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/manage')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>

          <Route path="/organizations/:orgId/user-feedback/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/userFeedback')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

          <Route path="/organizations/:orgId/issues/" component={errorHandler_1.default(container_1.default)}>
            <react_router_1.Redirect from="/organizations/:orgId/" to="/organizations/:orgId/issues/"/>
            <IndexRoute component={errorHandler_1.default(overview_1.default)}/>
            <Route path="searches/:searchId/" component={errorHandler_1.default(overview_1.default)}/>
          </Route>

          {/* Once org issues is complete, these routes can be nested under
        /organizations/:orgId/issues */}
          <Route path="/organizations/:orgId/issues/:groupId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEventDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.DETAILS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/activity/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupActivity')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.ACTIVITY,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/events/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEvents')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.EVENTS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/tags/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupTags')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.TAGS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/tags/:tagKey/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupTagValues')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.TAGS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/feedback/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupUserFeedback')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.USER_FEEDBACK,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/attachments/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEventAttachments')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.ATTACHMENTS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/similar/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupSimilarIssues')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.SIMILAR_ISSUES,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/merged/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupMerged')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.MERGED,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/grouping/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/grouping')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.GROUPING,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/events/:eventId/">
              <IndexRoute componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEventDetails')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.DETAILS,
            isEventRoute: true,
        }}/>
              <Route path="activity/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupActivity')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.ACTIVITY,
            isEventRoute: true,
        }}/>
              <Route path="events/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEvents')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.EVENTS,
            isEventRoute: true,
        }}/>
              <Route path="similar/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupSimilarIssues')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.SIMILAR_ISSUES,
            isEventRoute: true,
        }}/>
              <Route path="tags/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupTags')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.TAGS,
            isEventRoute: true,
        }}/>
              <Route path="tags/:tagKey/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupTagValues')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.TAGS,
            isEventRoute: true,
        }}/>
              <Route path="feedback/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupUserFeedback')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.USER_FEEDBACK,
            isEventRoute: true,
        }}/>
              <Route path="attachments/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupEventAttachments')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.ATTACHMENTS,
            isEventRoute: true,
        }}/>
              <Route path="merged/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/groupMerged')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.MERGED,
            isEventRoute: true,
        }}/>
              <Route path="grouping/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationGroupDetails/grouping')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)} props={{
            currentTab: header_1.TAB.GROUPING,
            isEventRoute: true,
        }}/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/alerts/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/list')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

            <Route path="rules/details/:ruleId/" name="Alert Rule Details" component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/rules/details')); }); }}/>

            <Route path="rules/">
              <IndexRoute component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/rules')); }); }}/>
              <Route path=":projectId/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/builder/projectProvider')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}>
                <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
                <Route path=":ruleId/" name="Edit Alert Rule" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/edit')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              </Route>
            </Route>

            <Route path="metric-rules/">
              <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
              <Route path=":projectId/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/builder/projectProvider')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}>
                <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
                <Route path=":ruleId/" name="Edit Alert Rule" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/edit')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              </Route>
            </Route>

            <Route path="rules/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/rules')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

            <Route path=":alertId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/details')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

            <Route path=":projectId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/builder/projectProvider')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
              <Route path="new/" name="New Alert Rule" component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/create')); }); }}/>
              <Route path="wizard/" name="Alert Creation Wizard" component={errorHandler_1.default(lazyLoad_1.default)} componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/alerts/wizard')); }); }}/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/monitors/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/monitors')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/monitors/monitors')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/monitors/create/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/monitors/create')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/monitors/:monitorId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/monitors/details')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/monitors/:monitorId/edit/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/monitors/edit')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>

          <Route path="/organizations/:orgId/releases/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases/list')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path=":release/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases/detail')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
              <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases/detail/overview')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              <Route path="commits/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases/detail/commits')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              <Route path="files-changed/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/releases/detail/filesChanged')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              <react_router_1.Redirect from="new-events/" to="/organizations/:orgId/releases/:release/"/>
              <react_router_1.Redirect from="all-events/" to="/organizations/:orgId/releases/:release/"/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/activity/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/organizationActivity')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

          <Route path="/organizations/:orgId/stats/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require(
            /* webpackChunkName: "OrganizationStats" */ 'app/views/organizationStats')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>

          <Route path="/organizations/:orgId/projects/:projectId/events/:eventId/" component={errorHandler_1.default(projectEventRedirect_1.default)}/>

          {/*
      TODO(mark) Long term this /queries route should go away and /discover should be the
      canoncial route for discover2. We have a redirect right now as /discover was for
      discover 1 and most of the application is linking to /discover/queries and not /discover
      */}
          <react_router_1.Redirect from="/organizations/:orgId/discover/" to="/organizations/:orgId/discover/queries/"/>
          <Route path="/organizations/:orgId/discover/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/eventsV2')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <Route path="queries/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/eventsV2/landing')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="results/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/eventsV2/results')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path=":eventSlug/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/eventsV2/eventDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/content')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/trends/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/trends')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/summary/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/transactionSummary')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/performance/summary/vitals/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/transactionSummary/transactionVitals')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/performance/summary/tags/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/transactionSummary/transactionTags')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="/organizations/:orgId/performance/summary/events/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/transactionSummary/transactionEvents')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/vitaldetail/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/vitalDetail')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/trace/:traceSlug/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/traceDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/:eventSlug/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/transactionDetails')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/performance/compare/:baselineEventSlug/:regressionEventSlug/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/performance/compare')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path="/organizations/:orgId/dashboards/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/create')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <Route path="widget/:widgetId/edit/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/widget')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="widget/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/widget')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <react_router_1.Redirect from="/organizations/:orgId/dashboards/:dashboardId/" to="/organizations/:orgId/dashboard/:dashboardId/"/>
          <Route path="/organizations/:orgId/dashboard/:dashboardId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/view')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <Route path="widget/:widgetId/edit/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/widget')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path="widget/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/dashboardsV2/widget')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>

          {/* Admin/manage routes */}
          <Route name="Admin" path="/manage/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminLayout')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminOverview')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Buffer" path="buffer/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminBuffer')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Relays" path="relays/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminRelays')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Organizations" path="organizations/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminOrganizations')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Projects" path="projects/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminProjects')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Queue" path="queue/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminQueue')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Quotas" path="quotas/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminQuotas')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Settings" path="settings/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminSettings')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Users" path="users/">
              <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminUsers')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              <Route path=":id" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminUserEdit')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            </Route>
            <Route name="Mail" path="status/mail/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminMail')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Environment" path="status/environment/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminEnvironment')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Packages" path="status/packages/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminPackages')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route name="Warnings" path="status/warnings/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/adminWarnings')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            {hook('routes:admin')}
          </Route>
        </Route>

        {/* The heavyweight organization detail views */}
        <Route path="/:orgId/" component={errorHandler_1.default(organizationDetails_1.default)}>
          <Route component={errorHandler_1.default(organizationRoot_1.default)}>
            {hook('routes:organization-root')}

            <Route path="/organizations/:orgId/projects/:projectId/getting-started/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/gettingStarted')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
              <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/overview')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
              <Route path=":platform/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/platformOrIntegration')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            </Route>

            <Route path="/organizations/:orgId/teams/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/teamCreate')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

            <Route path="/organizations/:orgId/">
              {hook('routes:organization')}
              <react_router_1.Redirect from="/organizations/:orgId/teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/your-teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/all-teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/" to="/settings/:orgId/teams/:teamId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/members/" to="/settings/:orgId/teams/:teamId/members/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/projects/" to="/settings/:orgId/teams/:teamId/projects/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/settings/" to="/settings/:orgId/teams/:teamId/settings/"/>
              <react_router_1.Redirect from="/organizations/:orgId/settings/" to="/settings/:orgId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/api-keys/" to="/settings/:orgId/api-keys/"/>
              <react_router_1.Redirect from="/organizations/:orgId/api-keys/:apiKey/" to="/settings/:orgId/api-keys/:apiKey/"/>
              <react_router_1.Redirect from="/organizations/:orgId/members/" to="/settings/:orgId/members/"/>
              <react_router_1.Redirect from="/organizations/:orgId/members/:memberId/" to="/settings/:orgId/members/:memberId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/rate-limits/" to="/settings/:orgId/rate-limits/"/>
              <react_router_1.Redirect from="/organizations/:orgId/repos/" to="/settings/:orgId/repos/"/>
            </Route>
            <Route path="/organizations/:orgId/projects/new/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/newProject')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
          <Route path=":projectId/getting-started/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/gettingStarted')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}>
            <IndexRoute componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/overview')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>
            <Route path=":platform/" componentPromise={function () {
            return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectInstall/platformOrIntegration')); });
        }} component={errorHandler_1.default(lazyLoad_1.default)}/>
          </Route>
        </Route>

        {/* A route tree for lightweight organizational detail views.
          This is strictly for deprecated URLs that we need to maintain */}
        <Route component={errorHandler_1.default(organizationDetails_1.LightWeightOrganizationDetails)}>
          {/* This is in the bottom lightweight group because "/organizations/:orgId/projects/new/" in heavyweight needs to be matched first */}
          <Route path="/organizations/:orgId/projects/:projectId/" componentPromise={function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/projectDetail')); }); }} component={errorHandler_1.default(lazyLoad_1.default)}/>

          <Route name="Organization" path="/:orgId/">
            <Route path=":projectId/">
              {/* Support for deprecated URLs (pre-Sentry 10). We just redirect users to new canonical URLs. */}
              <IndexRoute component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId;
            return "/organizations/" + orgId + "/issues/?project=" + projectId;
        }))}/>
              <Route path="issues/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId;
            return "/organizations/" + orgId + "/issues/?project=" + projectId;
        }))}/>
              <Route path="dashboard/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId;
            return "/organizations/" + orgId + "/dashboards/?project=" + projectId;
        }))}/>
              <Route path="user-feedback/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId;
            return "/organizations/" + orgId + "/user-feedback/?project=" + projectId;
        }))}/>
              <Route path="releases/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId;
            return "/organizations/" + orgId + "/releases/?project=" + projectId;
        }))}/>
              <Route path="releases/:version/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId, router = _a.router;
            return "/organizations/" + orgId + "/releases/" + router.params.version + "/?project=" + projectId;
        }))}/>
              <Route path="releases/:version/new-events/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId, router = _a.router;
            return "/organizations/" + orgId + "/releases/" + router.params.version + "/new-events/?project=" + projectId;
        }))}/>
              <Route path="releases/:version/all-events/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId, router = _a.router;
            return "/organizations/" + orgId + "/releases/" + router.params.version + "/all-events/?project=" + projectId;
        }))}/>
              <Route path="releases/:version/commits/" component={errorHandler_1.default(redirectDeprecatedProjectRoute_1.default(function (_a) {
            var orgId = _a.orgId, projectId = _a.projectId, router = _a.router;
            return "/organizations/" + orgId + "/releases/" + router.params.version + "/commits/?project=" + projectId;
        }))}/>
            </Route>
          </Route>
        </Route>

        <Route path="/:orgId/">
          <Route path=":projectId/settings/">
            <react_router_1.Redirect from="teams/" to="/settings/:orgId/projects/:projectId/teams/"/>
            <react_router_1.Redirect from="alerts/" to="/settings/:orgId/projects/:projectId/alerts/"/>
            <react_router_1.Redirect from="alerts/rules/" to="/settings/:orgId/projects/:projectId/alerts/rules/"/>
            <react_router_1.Redirect from="alerts/rules/new/" to="/settings/:orgId/projects/:projectId/alerts/rules/new/"/>
            <react_router_1.Redirect from="alerts/rules/:ruleId/" to="/settings/:orgId/projects/:projectId/alerts/rules/:ruleId/"/>
            <react_router_1.Redirect from="environments/" to="/settings/:orgId/projects/:projectId/environments/"/>
            <react_router_1.Redirect from="environments/hidden/" to="/settings/:orgId/projects/:projectId/environments/hidden/"/>
            <react_router_1.Redirect from="tags/" to="/settings/projects/:orgId/projects/:projectId/tags/"/>
            <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/projects/:projectId/issue-tracking/"/>
            <react_router_1.Redirect from="release-tracking/" to="/settings/:orgId/projects/:projectId/release-tracking/"/>
            <react_router_1.Redirect from="ownership/" to="/settings/:orgId/projects/:projectId/ownership/"/>
            <react_router_1.Redirect from="data-forwarding/" to="/settings/:orgId/projects/:projectId/data-forwarding/"/>
            <react_router_1.Redirect from="debug-symbols/" to="/settings/:orgId/projects/:projectId/debug-symbols/"/>
            <react_router_1.Redirect from="processing-issues/" to="/settings/:orgId/projects/:projectId/processing-issues/"/>
            <react_router_1.Redirect from="filters/" to="/settings/:orgId/projects/:projectId/filters/"/>
            <react_router_1.Redirect from="hooks/" to="/settings/:orgId/projects/:projectId/hooks/"/>
            <react_router_1.Redirect from="keys/" to="/settings/:orgId/projects/:projectId/keys/"/>
            <react_router_1.Redirect from="keys/:keyId/" to="/settings/:orgId/projects/:projectId/keys/:keyId/"/>
            <react_router_1.Redirect from="user-feedback/" to="/settings/:orgId/projects/:projectId/user-feedback/"/>
            <react_router_1.Redirect from="security-headers/" to="/settings/:orgId/projects/:projectId/security-headers/"/>
            <react_router_1.Redirect from="security-headers/csp/" to="/settings/:orgId/projects/:projectId/security-headers/csp/"/>
            <react_router_1.Redirect from="security-headers/expect-ct/" to="/settings/:orgId/projects/:projectId/security-headers/expect-ct/"/>
            <react_router_1.Redirect from="security-headers/hpkp/" to="/settings/:orgId/projects/:projectId/security-headers/hpkp/"/>
            <react_router_1.Redirect from="plugins/" to="/settings/:orgId/projects/:projectId/plugins/"/>
            <react_router_1.Redirect from="plugins/:pluginId/" to="/settings/:orgId/projects/:projectId/plugins/:pluginId/"/>
            <react_router_1.Redirect from="integrations/:providerKey/" to="/settings/:orgId/projects/:projectId/integrations/:providerKey/"/>
            <react_router_1.Redirect from="install/" to="/settings/:orgId/projects/:projectId/install/"/>
            <react_router_1.Redirect from="install/:platform'" to="/settings/:orgId/projects/:projectId/install/:platform/"/>
          </Route>
          <react_router_1.Redirect from=":projectId/group/:groupId/" to="issues/:groupId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/" to="/organizations/:orgId/issues/:groupId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/events/" to="/organizations/:orgId/issues/:groupId/events/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/events/:eventId/" to="/organizations/:orgId/issues/:groupId/events/:eventId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/tags/" to="/organizations/:orgId/issues/:groupId/tags/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/tags/:tagKey/" to="/organizations/:orgId/issues/:groupId/tags/:tagKey/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/feedback/" to="/organizations/:orgId/issues/:groupId/feedback/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/similar/" to="/organizations/:orgId/issues/:groupId/similar/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/merged/" to="/organizations/:orgId/issues/:groupId/merged/"/>
          <Route path=":projectId/events/:eventId/" component={errorHandler_1.default(projectEventRedirect_1.default)}/>
        </Route>

        {hook('routes')}
        <Route path="*" component={errorHandler_1.default(routeNotFound_1.default)} onEnter={appendTrailingSlash}/>
      </Route>
    </Route>);
}
exports.default = routes;
//# sourceMappingURL=routes.jsx.map