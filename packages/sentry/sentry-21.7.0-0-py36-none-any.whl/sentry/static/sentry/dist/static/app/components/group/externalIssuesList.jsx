Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var externalIssueActions_1 = tslib_1.__importDefault(require("app/components/group/externalIssueActions"));
var pluginActions_1 = tslib_1.__importDefault(require("app/components/group/pluginActions"));
var sentryAppExternalIssueActions_1 = tslib_1.__importDefault(require("app/components/group/sentryAppExternalIssueActions"));
var issueSyncListElement_1 = tslib_1.__importDefault(require("app/components/issueSyncListElement"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var externalIssueStore_1 = tslib_1.__importDefault(require("app/stores/externalIssueStore"));
var sentryAppComponentsStore_1 = tslib_1.__importDefault(require("app/stores/sentryAppComponentsStore"));
var sentryAppInstallationsStore_1 = tslib_1.__importDefault(require("app/stores/sentryAppInstallationsStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var sidebarSection_1 = tslib_1.__importDefault(require("./sidebarSection"));
var ExternalIssueList = /** @class */ (function (_super) {
    tslib_1.__extends(ExternalIssueList, _super);
    function ExternalIssueList(props) {
        var _this = _super.call(this, props, {}) || this;
        _this.unsubscribables = [];
        _this.onSentryAppInstallationChange = function (sentryAppInstallations) {
            _this.setState({ sentryAppInstallations: sentryAppInstallations });
        };
        _this.onExternalIssueChange = function (externalIssues) {
            _this.setState({ externalIssues: externalIssues });
        };
        _this.onSentryAppComponentsChange = function (sentryAppComponents) {
            var components = sentryAppComponents.filter(function (c) { return c.type === 'issue-link'; });
            _this.setState({ components: components });
        };
        _this.state = Object.assign({}, _this.state, {
            components: sentryAppComponentsStore_1.default.getInitialState(),
            sentryAppInstallations: sentryAppInstallationsStore_1.default.getInitialState(),
            externalIssues: externalIssueStore_1.default.getInitialState(),
        });
        return _this;
    }
    ExternalIssueList.prototype.getEndpoints = function () {
        var group = this.props.group;
        return [['integrations', "/groups/" + group.id + "/integrations/"]];
    };
    ExternalIssueList.prototype.UNSAFE_componentWillMount = function () {
        _super.prototype.UNSAFE_componentWillMount.call(this);
        this.unsubscribables = [
            sentryAppInstallationsStore_1.default.listen(this.onSentryAppInstallationChange, this),
            externalIssueStore_1.default.listen(this.onExternalIssueChange, this),
            sentryAppComponentsStore_1.default.listen(this.onSentryAppComponentsChange, this),
        ];
        this.fetchSentryAppData();
    };
    ExternalIssueList.prototype.componentWillUnmount = function () {
        _super.prototype.componentWillUnmount.call(this);
        this.unsubscribables.forEach(function (unsubscribe) { return unsubscribe(); });
    };
    // We want to do this explicitly so that we can handle errors gracefully,
    // instead of the entire component not rendering.
    //
    // Part of the API request here is fetching data from the Sentry App, so
    // we need to be more conservative about error cases since we don't have
    // control over those services.
    //
    ExternalIssueList.prototype.fetchSentryAppData = function () {
        var _this = this;
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization;
        if (project && project.id && organization) {
            this.api
                .requestPromise("/groups/" + group.id + "/external-issues/")
                .then(function (data) {
                externalIssueStore_1.default.load(data);
                _this.setState({ externalIssues: data });
            })
                .catch(function (_error) { });
        }
    };
    ExternalIssueList.prototype.updateIntegrations = function (onSuccess, onError) {
        if (onSuccess === void 0) { onSuccess = function () { }; }
        if (onError === void 0) { onError = function () { }; }
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var group, integrations, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        group = this.props.group;
                        return [4 /*yield*/, this.api.requestPromise("/groups/" + group.id + "/integrations/")];
                    case 1:
                        integrations = _a.sent();
                        this.setState({ integrations: integrations }, function () { return onSuccess(); });
                        return [3 /*break*/, 3];
                    case 2:
                        error_1 = _a.sent();
                        onError();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    ExternalIssueList.prototype.renderIntegrationIssues = function (integrations) {
        var _this = this;
        if (integrations === void 0) { integrations = []; }
        var group = this.props.group;
        var activeIntegrations = integrations.filter(function (integration) { return integration.status === 'active'; });
        var activeIntegrationsByProvider = activeIntegrations.reduce(function (acc, curr) {
            var items = acc.get(curr.provider.key);
            if (!!items) {
                acc.set(curr.provider.key, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(items)), [curr]));
            }
            else {
                acc.set(curr.provider.key, [curr]);
            }
            return acc;
        }, new Map());
        return activeIntegrations.length
            ? tslib_1.__spreadArray([], tslib_1.__read(activeIntegrationsByProvider.entries())).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), provider = _b[0], configurations = _b[1];
                return (<externalIssueActions_1.default key={provider} configurations={configurations} group={group} onChange={_this.updateIntegrations.bind(_this)}/>);
            })
            : null;
    };
    ExternalIssueList.prototype.renderSentryAppIssues = function () {
        var _this = this;
        var _a = this.state, externalIssues = _a.externalIssues, sentryAppInstallations = _a.sentryAppInstallations, components = _a.components;
        var group = this.props.group;
        if (components.length === 0) {
            return null;
        }
        return components.map(function (component) {
            var sentryApp = component.sentryApp;
            var installation = sentryAppInstallations.find(function (i) { return i.app.uuid === sentryApp.uuid; });
            // should always find a match but TS complains if we don't handle this case
            if (!installation) {
                return null;
            }
            var issue = (externalIssues || []).find(function (i) { return i.serviceType === sentryApp.slug; });
            return (<errorBoundary_1.default key={sentryApp.slug} mini>
          <sentryAppExternalIssueActions_1.default key={sentryApp.slug} group={group} event={_this.props.event} sentryAppComponent={component} sentryAppInstallation={installation} externalIssue={issue}/>
        </errorBoundary_1.default>);
        });
    };
    ExternalIssueList.prototype.renderPluginIssues = function () {
        var _a = this.props, group = _a.group, project = _a.project;
        return group.pluginIssues && group.pluginIssues.length
            ? group.pluginIssues.map(function (plugin, i) { return (<pluginActions_1.default group={group} project={project} plugin={plugin} key={i}/>); })
            : null;
    };
    ExternalIssueList.prototype.renderPluginActions = function () {
        var group = this.props.group;
        return group.pluginActions && group.pluginActions.length
            ? group.pluginActions.map(function (plugin, i) { return (<issueSyncListElement_1.default externalIssueLink={plugin[1]} key={i}>
            {plugin[0]}
          </issueSyncListElement_1.default>); })
            : null;
    };
    ExternalIssueList.prototype.renderLoading = function () {
        return (<sidebarSection_1.default data-test-id="linked-issues" title={locale_1.t('Linked Issues')}>
        <placeholder_1.default height="120px"/>
      </sidebarSection_1.default>);
    };
    ExternalIssueList.prototype.renderBody = function () {
        var sentryAppIssues = this.renderSentryAppIssues();
        var integrationIssues = this.renderIntegrationIssues(this.state.integrations);
        var pluginIssues = this.renderPluginIssues();
        var pluginActions = this.renderPluginActions();
        var showSetup = !sentryAppIssues && !integrationIssues && !pluginIssues && !pluginActions;
        return (<sidebarSection_1.default data-test-id="linked-issues" title={locale_1.t('Linked Issues')}>
        {showSetup && (<alertLink_1.default icon={<icons_1.IconGeneric />} priority="muted" size="small" to={"/settings/" + this.props.organization.slug + "/integrations"}>
            {locale_1.t('Set up Issue Tracking')}
          </alertLink_1.default>)}
        {sentryAppIssues && <Wrapper>{sentryAppIssues}</Wrapper>}
        {integrationIssues && <Wrapper>{integrationIssues}</Wrapper>}
        {pluginIssues && <Wrapper>{pluginIssues}</Wrapper>}
        {pluginActions && <Wrapper>{pluginActions}</Wrapper>}
      </sidebarSection_1.default>);
    };
    return ExternalIssueList;
}(asyncComponent_1.default));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
exports.default = withOrganization_1.default(ExternalIssueList);
var templateObject_1;
//# sourceMappingURL=externalIssuesList.jsx.map