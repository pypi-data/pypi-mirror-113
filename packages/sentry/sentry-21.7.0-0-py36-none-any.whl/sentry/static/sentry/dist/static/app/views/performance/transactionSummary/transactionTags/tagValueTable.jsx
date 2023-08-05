Object.defineProperty(exports, "__esModule", { value: true });
exports.TagValueTable = void 0;
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var gridEditable_1 = tslib_1.__importStar(require("app/components/gridEditable"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var iconAdd_1 = require("app/icons/iconAdd");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fields_1 = require("app/utils/discover/fields");
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = tslib_1.__importStar(require("app/views/eventsV2/table/cellAction"));
var utils_1 = require("../../utils");
var tagExplorer_1 = require("../tagExplorer");
var utils_2 = require("./utils");
var TAGS_CURSOR_NAME = 'tags_cursor';
var COLUMN_ORDER = [
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
        key: 'count',
        field: 'count',
        name: 'Events',
        width: -1,
        column: {
            kind: 'field',
        },
        canSort: true,
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
        key: 'action',
        field: 'action',
        name: '',
        width: -1,
        column: {
            kind: 'field',
        },
    },
];
var TagValueTable = /** @class */ (function (_super) {
    tslib_1.__extends(TagValueTable, _super);
    function TagValueTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.renderHeadCellWithMeta = function (sortedEventView, tableMeta, columns) {
            return function (column, index) {
                return _this.renderHeadCell(sortedEventView, tableMeta, column, columns[index]);
            };
        };
        _this.handleTagValueClick = function (location, tagKey, tagValue) {
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
                utils_2.trackTagPageInteraction(organization);
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
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
            var location = parentProps.location, eventView = parentProps.eventView, organization = parentProps.organization;
            if (column.key === 'key') {
                return dataRow.tags_key;
            }
            var allowActions = [cellAction_1.Actions.ADD, cellAction_1.Actions.EXCLUDE];
            if (column.key === 'tagValue') {
                var actionRow = tslib_1.__assign(tslib_1.__assign({}, dataRow), { id: dataRow.tags_key });
                return (<cellAction_1.default column={column} dataRow={actionRow} handleCellAction={_this.handleCellAction(column, dataRow.tags_value, actionRow)} allowActions={allowActions}>
          <tagExplorer_1.TagValue row={dataRow}/>
        </cellAction_1.default>);
            }
            if (column.key === 'frequency') {
                return <AlignRight>{formatters_1.formatPercentage(dataRow.frequency, 0)}</AlignRight>;
            }
            if (column.key === 'action') {
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
                var disabled = searchConditions.hasTag(dataRow.tags_key);
                return (<link_1.default disabled={disabled} to="" onClick={function () {
                        utils_2.trackTagPageInteraction(organization);
                        _this.handleTagValueClick(location, dataRow.tags_key, dataRow.tags_value);
                    }}>
          <LinkContainer>
            <iconAdd_1.IconAdd isCircled/>
            {locale_1.t('Add to filter')}
          </LinkContainer>
        </link_1.default>);
            }
            if (column.key === 'comparison') {
                var localValue = dataRow.comparison;
                var pct = formatters_1.formatPercentage(localValue - 1, 0);
                return localValue > 1 ? locale_1.t('+%s slower', pct) : locale_1.t('%s faster', pct);
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
            if (column.key === 'count') {
                return <AlignRight>{value}</AlignRight>;
            }
            return value;
        };
        _this.renderBodyCellWithData = function (parentProps) {
            return function (column, dataRow) {
                return _this.renderBodyCell(parentProps, column, dataRow);
            };
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = tslib_1.__spreadArray([], tslib_1.__read(_this.state.widths));
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : gridEditable_1.COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    TagValueTable.prototype.renderHeadCell = function (sortedEventView, tableMeta, column, columnInfo) {
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
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        return (<sortLink_1.default align={align} title={columnInfo.name} direction={currentSortKind} canSort={false} generateSortLink={generateSortLink} onClick={function () { }} // TODO(k-fish): Implement sorting
        />);
    };
    TagValueTable.prototype.render = function () {
        var _a = this.props, eventView = _a.eventView, tagKey = _a.tagKey, location = _a.location, isLoading = _a.isLoading, tableData = _a.tableData, aggregateColumn = _a.aggregateColumn;
        var newColumns = tslib_1.__spreadArray([], tslib_1.__read(COLUMN_ORDER)).map(function (c) {
            var newColumn = tslib_1.__assign({}, c);
            if (c.key === 'tagValue') {
                newColumn.name = tagKey;
            }
            if (c.key === 'aggregate') {
                if (aggregateColumn === 'measurements.lcp') {
                    newColumn.name = 'Avg LCP';
                }
            }
            return newColumn;
        });
        return (<StyledPanelTable>
        <gridEditable_1.default isLoading={isLoading} data={tableData && tableData.data ? tableData.data : []} columnOrder={newColumns} columnSortBy={[]} grid={{
                renderHeadCell: this.renderHeadCellWithMeta(eventView, tableData ? tableData.meta : {}, newColumns),
                renderBodyCell: this.renderBodyCellWithData(this.props),
                onResizeColumn: this.handleResizeColumn,
            }} location={location}/>
      </StyledPanelTable>);
    };
    return TagValueTable;
}(react_1.Component));
exports.TagValueTable = TagValueTable;
var StyledPanelTable = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  > div {\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n"], ["\n  > div {\n    border-top-left-radius: 0;\n    border-top-right-radius: 0;\n  }\n"])));
var AlignRight = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var LinkContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: flex-end;\n  align-items: center;\n"])), space_1.default(0.5));
exports.default = TagValueTable;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tagValueTable.jsx.map