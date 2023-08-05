var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.TagExplorer = exports.TagValue = exports.getTransactionField = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var guideAnchor_1 = require("app/components/assistant/guideAnchor");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var styles_1 = require("app/components/charts/styles");
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var gridEditable_1 = tslib_1.__importStar(require("app/components/gridEditable"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
var segmentExplorerQuery_1 = tslib_1.__importDefault(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = tslib_1.__importStar(require("app/views/eventsV2/table/cellAction"));
var utils_1 = require("../utils");
var utils_2 = require("./transactionTags/utils");
var filter_1 = require("./filter");
var TAGS_CURSOR_NAME = 'tags_cursor';
var COLUMN_ORDER = [
    {
        key: 'key',
        field: 'key',
        name: 'Tag Key',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'tagValue',
        field: 'tagValue',
        name: 'Tag Values',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'aggregate',
        field: 'aggregate',
        name: 'Avg Duration',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'frequency',
        field: 'frequency',
        name: 'Frequency',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'comparison',
        field: 'comparison',
        name: 'Compared To Avg',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
    {
        key: 'sumdelta',
        field: 'sumdelta',
        name: 'Total Time Lost',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
    },
];
var filterToField = (_a = {},
    _a[filter_1.SpanOperationBreakdownFilter.Browser] = 'spans.browser',
    _a[filter_1.SpanOperationBreakdownFilter.Http] = 'spans.http',
    _a[filter_1.SpanOperationBreakdownFilter.Db] = 'spans.db',
    _a[filter_1.SpanOperationBreakdownFilter.Resource] = 'spans.resource',
    _a);
var getTransactionField = function (currentFilter, projects, eventView) {
    var fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        return fieldFromFilter;
    }
    var performanceType = utils_1.platformAndConditionsToPerformanceType(projects, eventView);
    if (performanceType === utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        return 'measurements.lcp';
    }
    return 'transaction.duration';
};
exports.getTransactionField = getTransactionField;
var getColumnsWithReplacedDuration = function (currentFilter, projects, eventView) {
    var columns = COLUMN_ORDER.map(function (c) { return (tslib_1.__assign({}, c)); });
    var durationColumn = columns.find(function (c) { return c.key === 'aggregate'; });
    if (!durationColumn) {
        return columns;
    }
    var fieldFromFilter = filterToField[currentFilter];
    if (fieldFromFilter) {
        durationColumn.name = 'Avg Span Duration';
        return columns;
    }
    var performanceType = utils_1.platformAndConditionsToPerformanceType(projects, eventView);
    if (performanceType === utils_1.PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        durationColumn.name = 'Avg LCP';
        return columns;
    }
    return columns;
};
function TagValue(props) {
    return <div className="truncate">{props.row.tags_value}</div>;
}
exports.TagValue = TagValue;
var _TagExplorer = /** @class */ (function (_super) {
    tslib_1.__extends(_TagExplorer, _super);
    function _TagExplorer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = tslib_1.__spreadArray([], tslib_1.__read(_this.state.widths));
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        _this.getColumnOrder = function (columns) {
            var widths = _this.state.widths;
            return columns.map(function (col, i) {
                if (typeof widths[i] === 'number') {
                    return tslib_1.__assign(tslib_1.__assign({}, col), { width: widths[i] });
                }
                return col;
            });
        };
        _this.renderHeadCellWithMeta = function (sortedEventView, tableMeta, columns) {
            return function (column, index) {
                return _this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
            };
        };
        _this.handleTagValueClick = function (location, tagKey, tagValue) {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.summary.tag_explorer.tag_value',
                eventName: 'Performance Views: Tag Explorer Value Clicked',
                organization_id: parseInt(organization.id, 10),
            });
            var queryString = queryString_1.decodeScalar(location.query.query);
            var conditions = tokenizeSearch_1.tokenizeSearch(queryString || '');
            conditions.addTagValues(tagKey, [tagValue]);
            var query = conditions.formatString();
            react_router_1.browserHistory.push({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: String(query).trim() }),
            });
        };
        _this.handleCellAction = function (column, tagValue, actionRow) {
            return function (action) {
                var _a;
                var _b = _this.props, eventView = _b.eventView, location = _b.location, organization = _b.organization;
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'performance_views.summary.tag_explorer.cell_action',
                    eventName: 'Performance Views: Tag Explorer Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                });
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                cellAction_1.updateQuery(searchConditions, action, tslib_1.__assign(tslib_1.__assign({}, column), { name: actionRow.id }), tagValue);
                react_router_1.browserHistory.push({
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), (_a = {}, _a[TAGS_CURSOR_NAME] = undefined, _a.query = searchConditions.formatString(), _a)),
                });
            };
        };
        _this.renderBodyCell = function (parentProps, column, dataRow) {
            var value = dataRow[column.key];
            var location = parentProps.location, organization = parentProps.organization, transactionName = parentProps.transactionName;
            if (column.key === 'key') {
                var target_1 = utils_2.tagsRouteWithQuery({
                    orgSlug: organization.slug,
                    transaction: transactionName,
                    projectID: queryString_1.decodeScalar(location.query.project),
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { tagKey: dataRow.tags_key }),
                });
                return (<feature_1.default features={['performance-tag-page']} organization={organization}>
          {function (_a) {
                        var hasFeature = _a.hasFeature;
                        if (hasFeature) {
                            return (<link_1.default to={target_1} onClick={function () { return _this.onTagKeyClick(); }}>
                  {dataRow.tags_key}
                </link_1.default>);
                        }
                        return dataRow.tags_key;
                    }}
        </feature_1.default>);
            }
            var allowActions = [cellAction_1.Actions.ADD, cellAction_1.Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                var actionRow = tslib_1.__assign(tslib_1.__assign({}, dataRow), { id: dataRow.tags_key });
                return (<cellAction_1.default column={column} dataRow={actionRow} handleCellAction={_this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <feature_1.default features={['performance-tag-page']} organization={organization}>
            {function (_a) {
                        var hasFeature = _a.hasFeature;
                        if (hasFeature) {
                            return <div className="truncate">{dataRow.tags_value}</div>;
                        }
                        return (<link_1.default to="" onClick={function () {
                                return _this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value);
                            }}>
                  <TagValue row={dataRow}/>
                </link_1.default>);
                    }}
          </feature_1.default>
        </cellAction_1.default>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{formatters_1.formatPercentage(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'comparison') {
                var localValue = dataRow.comparison;
                var pct = formatters_1.formatPercentage(localValue - 1, 0);
                return (<AlignRight>
          {localValue > 1 ? locale_1.t('+%s slower', pct) : locale_1.t('%s faster', pct)}
        </AlignRight>);
            }
            if (column.key === 'aggregate') {
                return (<AlignRight>
          <utils_1.PerformanceDuration abbreviation milliseconds={dataRow.aggregate}/>
        </AlignRight>);
            }
            if (column.key === 'sumdelta') {
                return (<AlignRight>
          <utils_1.PerformanceDuration abbreviation milliseconds={dataRow.sumdelta}/>
        </AlignRight>);
            }
            return value;
        };
        _this.renderBodyCellWithData = function (parentProps) {
            return function (column, dataRow) {
                return _this.renderBodyCell(parentProps, column, dataRow);
            };
        };
        return _this;
    }
    _TagExplorer.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.sort',
            eventName: 'Performance Views: Tag Explorer Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    _TagExplorer.prototype.renderHeadCell = function (sortedEventView, tableMeta, column, columnInfo) {
        var _this = this;
        var location = this.props.location;
        var align = fields_1.fieldAlignment(column.key, column.type, tableMeta);
        var field = { field: column.key, width: column.width };
        function generateSortLink() {
            var _a;
            if (!tableMeta) {
                return undefined;
            }
            var nextEventView = sortedEventView.sortOnField(field, tableMeta);
            var sort = nextEventView.generateQueryStringObject().sort;
            return tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), (_a = {}, _a[TAGS_CURSOR_NAME] = undefined, _a.tagSort = sort, _a)) });
        }
        var currentSort = sortedEventView.sortForField(field, tableMeta);
        var canSort = eventView_1.isFieldSortable(field, tableMeta);
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        return (<sortLink_1.default align={align} title={columnInfo.name} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
    };
    _TagExplorer.prototype.onTagKeyClick = function () {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.visit_tag_key',
            eventName: 'Performance Views: Tag Explorer - Visit Tag Key',
            organization_id: parseInt(organization.id, 10),
        });
    };
    _TagExplorer.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, eventView = _c.eventView, organization = _c.organization, location = _c.location, currentFilter = _c.currentFilter, projects = _c.projects, transactionName = _c.transactionName;
        var tagSort = queryString_1.decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a.tagSort);
        var cursor = queryString_1.decodeScalar((_b = location.query) === null || _b === void 0 ? void 0 : _b[TAGS_CURSOR_NAME]);
        var tagEventView = eventView.clone();
        tagEventView.fields = COLUMN_ORDER;
        var tagSorts = eventView_1.fromSorts(tagSort);
        var sortedEventView = tagEventView.withSorts(tagSorts.length
            ? tagSorts
            : [
                {
                    field: 'sumdelta',
                    kind: 'desc',
                },
            ]);
        var aggregateColumn = exports.getTransactionField(currentFilter, projects, sortedEventView);
        var adjustedColumns = getColumnsWithReplacedDuration(currentFilter, projects, sortedEventView);
        var columns = this.getColumnOrder(adjustedColumns);
        var columnSortBy = sortedEventView.getSorts();
        return (<segmentExplorerQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={5} cursor={cursor}>
        {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
              <guideAnchor_1.GuideAnchor target="tag_explorer">
                <TagsHeader transactionName={transactionName} location={location} organization={organization} pageLinks={pageLinks}/>
              </guideAnchor_1.GuideAnchor>
              <gridEditable_1.default isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={columns} columnSortBy={columnSortBy} grid={{
                        renderHeadCell: _this.renderHeadCellWithMeta(sortedEventView, (tableData === null || tableData === void 0 ? void 0 : tableData.meta) || {}, adjustedColumns),
                        renderBodyCell: _this.renderBodyCellWithData(_this.props),
                        onResizeColumn: _this.handleResizeColumn,
                    }} location={location}/>
            </React.Fragment>);
            }}
      </segmentExplorerQuery_1.default>);
    };
    return _TagExplorer;
}(React.Component));
function TagsHeader(props) {
    var pageLinks = props.pageLinks, organization = props.organization, location = props.location, transactionName = props.transactionName;
    var handleCursor = function (cursor, pathname, query) {
        var _a;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.change_page',
            eventName: 'Performance Views: Tag Explorer Change Page',
            organization_id: parseInt(organization.id, 10),
        });
        react_router_1.browserHistory.push({
            pathname: pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, query), (_a = {}, _a[TAGS_CURSOR_NAME] = cursor, _a)),
        });
    };
    var handleViewAllTagsClick = function () {
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.summary.tag_explorer.change_page',
            eventName: 'Performance Views: Tag Explorer Change Page',
            organization_id: parseInt(organization.id, 10),
        });
    };
    var viewAllTarget = utils_2.tagsRouteWithQuery({
        orgSlug: organization.slug,
        transaction: transactionName,
        projectID: queryString_1.decodeScalar(location.query.project),
        query: tslib_1.__assign({}, location.query),
    });
    return (<Header>
      <div>
        <styles_1.SectionHeading>{locale_1.t('Suspect Tags')}</styles_1.SectionHeading>
        <featureBadge_1.default type="beta"/>
      </div>
      <feature_1.default features={['performance-tag-page']} organization={organization}>
        <button_1.default onClick={handleViewAllTagsClick} to={viewAllTarget} size="small" data-test-id="tags-explorer-open-tags">
          {locale_1.t('View All Tags')}
        </button_1.default>
      </feature_1.default>
      <StyledPagination pageLinks={pageLinks} onCursor={handleCursor} size="small"/>
    </Header>);
}
var AlignRight = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto auto;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var StyledPagination = styled_1.default(pagination_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0 0 0 ", ";\n"], ["\n  margin: 0 0 0 ", ";\n"])), space_1.default(1));
exports.TagExplorer = _TagExplorer;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tagExplorer.jsx.map