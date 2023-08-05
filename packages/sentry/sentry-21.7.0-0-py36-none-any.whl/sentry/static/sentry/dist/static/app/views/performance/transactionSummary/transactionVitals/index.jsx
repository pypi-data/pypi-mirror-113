Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var fields_1 = require("app/utils/discover/fields");
var constants_1 = require("app/utils/performance/vitals/constants");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var utils_1 = require("../../utils");
var constants_2 = require("./constants");
var content_1 = tslib_1.__importDefault(require("./content"));
var TransactionVitals = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionVitals, _super);
    function TransactionVitals() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateRumEventView(_this.props.location, utils_1.getTransactionName(_this.props.location)),
        };
        _this.renderNoAccess = function () {
            return <alert_1.default type="warning">{locale_1.t("You don't have access to this feature")}</alert_1.default>;
        };
        return _this;
    }
    TransactionVitals.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { eventView: generateRumEventView(nextProps.location, utils_1.getTransactionName(nextProps.location)) });
    };
    TransactionVitals.prototype.getDocumentTitle = function () {
        var name = utils_1.getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), locale_1.t('Vitals')].join(' \u2014 ');
        }
        return [locale_1.t('Summary'), locale_1.t('Vitals')].join(' \u2014 ');
    };
    TransactionVitals.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = utils_1.getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: tslib_1.__assign({}, location.query),
            });
            return null;
        }
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <feature_1.default features={['performance-view']} organization={organization} renderDisabled={this.renderNoAccess}>
          <globalSelectionHeader_1.default lockedMessageSubject={locale_1.t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
            <StyledPageContent>
              <lightWeightNoProjectMessage_1.default organization={organization}>
                <content_1.default location={location} eventView={eventView} transactionName={transactionName} organization={organization} projects={projects}/>
              </lightWeightNoProjectMessage_1.default>
            </StyledPageContent>
          </globalSelectionHeader_1.default>
        </feature_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return TransactionVitals;
}(react_1.Component));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateRumEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    var query = queryString_1.decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch_1.tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction.op', ['pageload'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (fields_1.isAggregateField(field))
            conditions.removeTag(field);
    });
    var vitals = constants_2.VITAL_GROUPS.reduce(function (allVitals, group) {
        return allVitals.concat(group.vitals);
    }, []);
    return eventView_1.default.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(vitals.map(function (vital) { return "percentile(" + vital + ", " + constants_2.PERCENTILE + ")"; }))), tslib_1.__read(vitals.map(function (vital) { return "count_at_least(" + vital + ", 0)"; }))), tslib_1.__read(vitals.map(function (vital) { return "count_at_least(" + vital + ", " + constants_1.WEB_VITAL_DETAILS[vital].poorThreshold + ")"; }))),
        query: conditions.formatString(),
        projects: [],
    }, location);
}
exports.default = withGlobalSelection_1.default(withProjects_1.default(withOrganization_1.default(TransactionVitals)));
var templateObject_1;
//# sourceMappingURL=index.jsx.map