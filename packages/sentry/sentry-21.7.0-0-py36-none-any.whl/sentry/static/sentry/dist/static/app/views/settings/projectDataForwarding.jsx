Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var pluginList_1 = tslib_1.__importDefault(require("app/components/pluginList"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var DataForwardingStats = /** @class */ (function (_super) {
    tslib_1.__extends(DataForwardingStats, _super);
    function DataForwardingStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DataForwardingStats.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        var options = {
            query: {
                since: since,
                until: until,
                resolution: '1d',
                stat: 'forwarded',
            },
        };
        return [['stats', "/projects/" + orgId + "/" + projectId + "/stats/", options]];
    };
    DataForwardingStats.prototype.renderBody = function () {
        var projectId = this.props.params.projectId;
        var stats = this.state.stats;
        var series = {
            seriesName: locale_1.t('Forwarded'),
            data: stats.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], value = _b[1];
                return ({ name: timestamp * 1000, value: value });
            }),
        };
        var forwardedAny = series.data.some(function (_a) {
            var value = _a.value;
            return value > 0;
        });
        return (<panels_1.Panel>
        <sentryDocumentTitle_1.default title={locale_1.t('Data Forwarding')} projectSlug={projectId}/>
        <panels_1.PanelHeader>{locale_1.t('Forwarded events in the last 30 days (by day)')}</panels_1.PanelHeader>
        <panels_1.PanelBody withPadding>
          {forwardedAny ? (<miniBarChart_1.default isGroupedByDate showTimeInTooltip labelYAxisExtents series={[series]} height={150}/>) : (<emptyMessage_1.default title={locale_1.t('Nothing forwarded in the last 30 days.')} description={locale_1.t('Total events forwarded to third party integrations.')}/>)}
        </panels_1.PanelBody>
      </panels_1.Panel>);
    };
    return DataForwardingStats;
}(asyncComponent_1.default));
var ProjectDataForwarding = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectDataForwarding, _super);
    function ProjectDataForwarding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onEnablePlugin = function (plugin) { return _this.updatePlugin(plugin, true); };
        _this.onDisablePlugin = function (plugin) { return _this.updatePlugin(plugin, false); };
        return _this;
    }
    ProjectDataForwarding.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['plugins', "/projects/" + orgId + "/" + projectId + "/plugins/"]];
    };
    Object.defineProperty(ProjectDataForwarding.prototype, "forwardingPlugins", {
        get: function () {
            return this.state.plugins.filter(function (p) { return p.type === 'data-forwarding' && p.hasConfiguration; });
        },
        enumerable: false,
        configurable: true
    });
    ProjectDataForwarding.prototype.updatePlugin = function (plugin, enabled) {
        var plugins = this.state.plugins.map(function (p) { return (tslib_1.__assign(tslib_1.__assign({}, p), { enabled: p.id === plugin.id ? enabled : p.enabled })); });
        this.setState({ plugins: plugins });
    };
    ProjectDataForwarding.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, project = _a.project;
        var plugins = this.forwardingPlugins;
        var hasAccess = organization.access.includes('project:write');
        var pluginsPanel = plugins.length > 0 ? (<pluginList_1.default organization={organization} project={project} pluginList={plugins} onEnablePlugin={this.onEnablePlugin} onDisablePlugin={this.onDisablePlugin}/>) : (<panels_1.Panel>
          <emptyMessage_1.default title={locale_1.t('There are no integrations available for data forwarding')}/>
        </panels_1.Panel>);
        return (<div data-test-id="data-forwarding-settings">
        <feature_1.default features={['projects:data-forwarding']} hookName="feature-disabled:data-forwarding">
          {function (_a) {
                var hasFeature = _a.hasFeature, features = _a.features;
                return (<react_1.Fragment>
              <settingsPageHeader_1.default title={locale_1.t('Data Forwarding')}/>
              <textBlock_1.default>
                {locale_1.tct("Data Forwarding allows processed events to be sent to your\n                favorite business intelligence tools. The exact payload and\n                types of data depend on the integration you're using. Learn\n                more about this functionality in our [link:documentation].", {
                        link: (<externalLink_1.default href="https://docs.sentry.io/product/data-management-settings/data-forwarding/"/>),
                    })}
              </textBlock_1.default>
              <permissionAlert_1.default />

              <alert_1.default icon={<icons_1.IconInfo size="md"/>}>
                {locale_1.tct("Sentry forwards [em:all applicable events] to the provider, in\n                some cases this may be a significant volume of data.", {
                        em: <strong />,
                    })}
              </alert_1.default>

              {!hasFeature && (<featureDisabled_1.default alert featureName="Data Forwarding" features={features}/>)}

              <DataForwardingStats params={params}/>
              {hasAccess && hasFeature && pluginsPanel}
            </react_1.Fragment>);
            }}
        </feature_1.default>
      </div>);
    };
    return ProjectDataForwarding;
}(asyncComponent_1.default));
exports.default = withOrganization_1.default(ProjectDataForwarding);
//# sourceMappingURL=projectDataForwarding.jsx.map