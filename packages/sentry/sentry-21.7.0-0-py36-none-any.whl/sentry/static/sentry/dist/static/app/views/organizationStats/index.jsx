Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationStats = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var pageTimeRangeSelector_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector/pageTimeRangeSelector"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var usageChart_1 = require("./usageChart");
var usageStatsOrg_1 = tslib_1.__importDefault(require("./usageStatsOrg"));
var usageStatsProjects_1 = tslib_1.__importDefault(require("./usageStatsProjects"));
var PAGE_QUERY_PARAMS = [
    'pageStatsPeriod',
    'pageStart',
    'pageEnd',
    'pageUtc',
    'dataCategory',
    'transform',
    'sort',
    'query',
    'cursor',
];
var OrganizationStats = /** @class */ (function (_super) {
    tslib_1.__extends(OrganizationStats, _super);
    function OrganizationStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getNextLocations = function (project) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var nextLocation = tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { project: project.id }) });
            // Do not leak out page-specific keys
            nextLocation.query = omit_1.default(nextLocation.query, PAGE_QUERY_PARAMS);
            return {
                performance: tslib_1.__assign(tslib_1.__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/performance/" }),
                projectDetail: tslib_1.__assign(tslib_1.__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/projects/" + project.slug + "/" }),
                issueList: tslib_1.__assign(tslib_1.__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/issues/" }),
                settings: {
                    pathname: "/settings/" + organization.slug + "/projects/" + project.slug + "/",
                },
            };
        };
        _this.handleUpdateDatetime = function (datetime) {
            var start = datetime.start, end = datetime.end, relative = datetime.relative, utc = datetime.utc;
            if (start && end) {
                var parser = utc ? moment_1.default.utc : moment_1.default;
                return _this.setStateOnUrl({
                    pageStatsPeriod: undefined,
                    pageStart: parser(start).format(),
                    pageEnd: parser(end).format(),
                    pageUtc: utc !== null && utc !== void 0 ? utc : undefined,
                });
            }
            return _this.setStateOnUrl({
                pageStatsPeriod: relative || undefined,
                pageStart: undefined,
                pageEnd: undefined,
                pageUtc: undefined,
            });
        };
        /**
         * TODO: Enable user to set dateStart/dateEnd
         *
         * See PAGE_QUERY_PARAMS for list of accepted keys on nextState
         */
        _this.setStateOnUrl = function (nextState, options) {
            if (options === void 0) { options = {
                willUpdateRouter: true,
            }; }
            var _a = _this.props, location = _a.location, router = _a.router;
            var nextQueryParams = pick_1.default(nextState, PAGE_QUERY_PARAMS);
            var nextLocation = tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location === null || location === void 0 ? void 0 : location.query), nextQueryParams) });
            if (options.willUpdateRouter) {
                router.push(nextLocation);
            }
            return nextLocation;
        };
        _this.renderPageControl = function () {
            var organization = _this.props.organization;
            var _a = _this.dataDatetime, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc;
            return (<react_1.Fragment>
        <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={_this.handleUpdateDatetime} relativeOptions={omit_1.default(constants_1.DEFAULT_RELATIVE_PERIODS, ['1h'])}/>

        <DropdownDataCategory label={<DropdownLabel>
              <span>{locale_1.t('Event Type: ')}</span>
              <span>{_this.dataCategoryName}</span>
            </DropdownLabel>}>
          {usageChart_1.CHART_OPTIONS_DATACATEGORY.map(function (option) { return (<dropdownControl_1.DropdownItem key={option.value} eventKey={option.value} onSelect={function (val) {
                        return _this.setStateOnUrl({ dataCategory: val });
                    }}>
              {option.label}
            </dropdownControl_1.DropdownItem>); })}
        </DropdownDataCategory>
      </react_1.Fragment>);
        };
        return _this;
    }
    Object.defineProperty(OrganizationStats.prototype, "dataCategory", {
        get: function () {
            var _a, _b;
            var dataCategory = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.dataCategory;
            switch (dataCategory) {
                case types_1.DataCategory.ERRORS:
                case types_1.DataCategory.TRANSACTIONS:
                case types_1.DataCategory.ATTACHMENTS:
                    return dataCategory;
                default:
                    return types_1.DataCategory.ERRORS;
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataCategoryName", {
        get: function () {
            var _a;
            var dataCategory = this.dataCategory;
            return (_a = types_1.DataCategoryName[dataCategory]) !== null && _a !== void 0 ? _a : locale_1.t('Unknown Data Category');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataDatetime", {
        get: function () {
            var _a, _b;
            var query = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) !== null && _b !== void 0 ? _b : {};
            var _c = getParams_1.getParams(query, {
                allowEmptyPeriod: true,
                allowAbsoluteDatetime: true,
                allowAbsolutePageDatetime: true,
            }), start = _c.start, end = _c.end, statsPeriod = _c.statsPeriod, utcString = _c.utc;
            if (!statsPeriod && !start && !end) {
                return { period: constants_1.DEFAULT_STATS_PERIOD };
            }
            // Following getParams, statsPeriod will take priority over start/end
            if (statsPeriod) {
                return { period: statsPeriod };
            }
            var utc = utcString === 'true';
            if (start && end) {
                return utc
                    ? {
                        start: moment_1.default.utc(start).format(),
                        end: moment_1.default.utc(end).format(),
                        utc: utc,
                    }
                    : {
                        start: moment_1.default(start).utc().format(),
                        end: moment_1.default(end).utc().format(),
                        utc: utc,
                    };
            }
            return { period: constants_1.DEFAULT_STATS_PERIOD };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "chartTransform", {
        // Validation and type-casting should be handled by chart
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.transform;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableSort", {
        // Validation and type-casting should be handled by table
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.sort;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableQuery", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.query;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableCursor", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.cursor;
        },
        enumerable: false,
        configurable: true
    });
    OrganizationStats.prototype.render = function () {
        var organization = this.props.organization;
        return (<sentryDocumentTitle_1.default title="Usage Stats">
        <organization_1.PageContent>
          <organization_1.PageHeader>
            <pageHeading_1.default>{locale_1.t('Organization Usage Stats')}</pageHeading_1.default>
          </organization_1.PageHeader>

          <p>
            {locale_1.t('We collect usage metrics on three types of events: errors, transactions, and attachments. The charts below reflect events that Sentry has received across your entire organization. You can also find them broken down by project in the table.')}
          </p>

          <PageGrid>
            {this.renderPageControl()}

            <errorBoundary_1.default mini>
              <usageStatsOrg_1.default organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} chartTransform={this.chartTransform} handleChangeState={this.setStateOnUrl}/>
            </errorBoundary_1.default>
            <errorBoundary_1.default mini>
              <usageStatsProjects_1.default organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} tableSort={this.tableSort} tableQuery={this.tableQuery} tableCursor={this.tableCursor} handleChangeState={this.setStateOnUrl} getNextLocations={this.getNextLocations}/>
            </errorBoundary_1.default>
          </PageGrid>
        </organization_1.PageContent>
      </sentryDocumentTitle_1.default>);
    };
    return OrganizationStats;
}(react_1.Component));
exports.OrganizationStats = OrganizationStats;
exports.default = withOrganization_1.default(OrganizationStats);
var PageGrid = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, 1fr);\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var DropdownDataCategory = styled_1.default(dropdownControl_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 42px;\n  grid-column: auto / span 1;\n  justify-self: stretch;\n  align-self: stretch;\n\n  button {\n    width: 100%;\n    height: 100%;\n\n    > span {\n      display: flex;\n      justify-content: space-between;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 1;\n  }\n"], ["\n  height: 42px;\n  grid-column: auto / span 1;\n  justify-self: stretch;\n  align-self: stretch;\n\n  button {\n    width: 100%;\n    height: 100%;\n\n    > span {\n      display: flex;\n      justify-content: space-between;\n    }\n  }\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 1;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var StyledPageTimeRangeSelector = styled_1.default(pageTimeRangeSelector_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  grid-column: auto / span 1;\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 3;\n  }\n"], ["\n  grid-column: auto / span 1;\n\n  @media (min-width: ", ") {\n    grid-column: auto / span 2;\n  }\n  @media (min-width: ", ") {\n    grid-column: auto / span 3;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var DropdownLabel = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"], ["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map