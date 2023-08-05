Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var qs = tslib_1.__importStar(require("query-string"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var monitorIcon_1 = tslib_1.__importDefault(require("./monitorIcon"));
var Monitors = /** @class */ (function (_super) {
    tslib_1.__extends(Monitors, _super);
    function Monitors() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var router = _this.context.router;
            router.push({
                pathname: location.pathname,
                query: getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query })),
            });
        };
        return _this;
    }
    Monitors.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [
            [
                'monitorList',
                "/organizations/" + params.orgId + "/monitors/",
                {
                    query: location.query,
                },
            ],
        ];
    };
    Monitors.prototype.getTitle = function () {
        return "Monitors - " + this.props.params.orgId;
    };
    Monitors.prototype.renderBody = function () {
        var _a;
        var _b = this.state, monitorList = _b.monitorList, monitorListPageLinks = _b.monitorListPageLinks;
        var organization = this.props.organization;
        return (<react_1.Fragment>
        <organization_1.PageHeader>
          <HeaderTitle>
            <div>
              {locale_1.t('Monitors')} <featureBadge_1.default type="beta"/>
            </div>
            <NewMonitorButton to={"/organizations/" + organization.slug + "/monitors/create/"} priority="primary" size="xsmall">
              {locale_1.t('New Monitor')}
            </NewMonitorButton>
          </HeaderTitle>
          <StyledSearchBar query={queryString_1.decodeScalar((_a = qs.parse(location.search)) === null || _a === void 0 ? void 0 : _a.query, '')} placeholder={locale_1.t('Search for monitors.')} onSearch={this.handleSearch}/>
        </organization_1.PageHeader>
        <panels_1.Panel>
          <panels_1.PanelBody>
            {monitorList === null || monitorList === void 0 ? void 0 : monitorList.map(function (monitor) { return (<PanelItemCentered key={monitor.id}>
                <monitorIcon_1.default status={monitor.status} size={16}/>
                <StyledLink to={"/organizations/" + organization.slug + "/monitors/" + monitor.id + "/"}>
                  {monitor.name}
                </StyledLink>
                {monitor.nextCheckIn ? (<timeSince_1.default date={monitor.lastCheckIn}/>) : (locale_1.t('n/a'))}
              </PanelItemCentered>); })}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {monitorListPageLinks && (<pagination_1.default pageLinks={monitorListPageLinks} {...this.props}/>)}
      </react_1.Fragment>);
    };
    return Monitors;
}(asyncView_1.default));
var HeaderTitle = styled_1.default(pageHeading_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex: 1;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex: 1;\n"])));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var NewMonitorButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(2));
var PanelItemCentered = styled_1.default(panels_1.PanelItem)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  align-items: center;\n  padding: 0;\n  padding-left: ", ";\n  padding-right: ", ";\n"], ["\n  align-items: center;\n  padding: 0;\n  padding-left: ", ";\n  padding-right: ", ";\n"])), space_1.default(2), space_1.default(2));
var StyledLink = styled_1.default(react_router_1.Link)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space_1.default(2));
exports.default = react_router_1.withRouter(withOrganization_1.default(Monitors));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=monitors.jsx.map