Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var tags_1 = require("app/actionCreators/tags");
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var fields_1 = require("app/utils/discover/fields");
var queryString_1 = require("app/utils/queryString");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var data_1 = require("../data");
var utils_1 = require("../utils");
var vitalDetailContent_1 = tslib_1.__importDefault(require("./vitalDetailContent"));
var VitalDetail = /** @class */ (function (_super) {
    tslib_1.__extends(VitalDetail, _super);
    function VitalDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: data_1.generatePerformanceVitalDetailView(_this.props.organization, _this.props.location),
        };
        return _this;
    }
    VitalDetail.getDerivedStateFromProps = function (nextProps, prevState) {
        return tslib_1.__assign(tslib_1.__assign({}, prevState), { eventView: data_1.generatePerformanceVitalDetailView(nextProps.organization, nextProps.location) });
    };
    VitalDetail.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        tags_1.loadOrganizationTags(api, organization.slug, selection);
        utils_1.addRoutePerformanceContext(selection);
    };
    VitalDetail.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual_1.default(prevProps.selection.projects, selection.projects) ||
            !isEqual_1.default(prevProps.selection.datetime, selection.datetime)) {
            tags_1.loadOrganizationTags(api, organization.slug, selection);
            utils_1.addRoutePerformanceContext(selection);
        }
    };
    VitalDetail.prototype.getDocumentTitle = function () {
        var name = utils_1.getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), locale_1.t('Performance')].join(' - ');
        }
        return [locale_1.t('Vital Detail'), locale_1.t('Performance')].join(' - ');
    };
    VitalDetail.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router;
        var eventView = this.state.eventView;
        if (!eventView) {
            react_router_1.browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: tslib_1.__assign({}, location.query),
            });
            return null;
        }
        var vitalNameQuery = queryString_1.decodeScalar(location.query.vitalName);
        var vitalName = Object.values(fields_1.WebVital).indexOf(vitalNameQuery) === -1
            ? undefined
            : vitalNameQuery;
        return (<sentryDocumentTitle_1.default title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <globalSelectionHeader_1.default>
          <StyledPageContent>
            <lightWeightNoProjectMessage_1.default organization={organization}>
              <vitalDetailContent_1.default location={location} organization={organization} eventView={eventView} router={router} vitalName={vitalName || fields_1.WebVital.LCP}/>
            </lightWeightNoProjectMessage_1.default>
          </StyledPageContent>
        </globalSelectionHeader_1.default>
      </sentryDocumentTitle_1.default>);
    };
    return VitalDetail;
}(react_1.Component));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
exports.default = withApi_1.default(withGlobalSelection_1.default(withProjects_1.default(withOrganization_1.default(VitalDetail))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map