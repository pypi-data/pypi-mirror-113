Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectID = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var gridEditable_1 = tslib_1.__importStar(require("app/components/gridEditable"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var eventView_1 = require("app/utils/discover/eventView");
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = tslib_1.__importStar(require("app/views/eventsV2/table/cellAction"));
var data_1 = require("../../data");
var utils_2 = require("../utils");
var operationSort_1 = tslib_1.__importDefault(require("./operationSort"));
function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
exports.getProjectID = getProjectID;
var OperationTitle = /** @class */ (function (_super) {
    tslib_1.__extends(OperationTitle, _super);
    function OperationTitle() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OperationTitle.prototype.render = function () {
        var onClick = this.props.onClick;
        return (<div onClick={onClick}>
        <span>{locale_1.t('operation duration')}</span>
        <StyledIconQuestion size="xs" position="top" title={locale_1.t("Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.")}/>
      </div>);
    };
    return OperationTitle;
}(React.Component));
var EventsTable = /** @class */ (function (_super) {
    tslib_1.__extends(EventsTable, _super);
    function EventsTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'performance_views.transactionEvents.cellaction',
                    eventName: 'Performance Views: Transaction Events Tab Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                var searchConditions = tokenizeSearch_1.tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                cellAction_1.updateQuery(searchConditions, action, column, value);
                ReactRouter.browserHistory.push({
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: searchConditions.formatString() }),
                });
            };
        };
        _this.renderBodyCellWithData = function (tableData) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta) {
            var _a;
            var columnTitles = (_a = _this.props.columnTitles) !== null && _a !== void 0 ? _a : data_1.COLUMN_TITLES;
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, columnTitles[index]);
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
    EventsTable.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, transactionName = _a.transactionName;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = fieldRenderers_1.getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location, eventView: eventView });
        var allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
        ];
        if (field === 'id' || field === 'trace') {
            var generateLink = field === 'id' ? utils_2.generateTransactionLink : utils_2.generateTraceLink;
            var target = generateLink(transactionName)(organization, dataRow, location.query);
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <link_1.default to={target}>{rendered}</link_1.default>
        </cellAction_1.default>);
        }
        var fieldName = fields_1.getAggregateAlias(field);
        var value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && utils_1.defined(value) && value > 999) {
            return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
            {rendered}
          </cellAction_1.default>
        </tooltip_1.default>);
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
    };
    EventsTable.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.transactionEvents.sort',
            eventName: 'Performance Views: Transaction Events Tab Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    EventsTable.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location;
        var align = fields_1.fieldAlignment(column.name, column.type, tableMeta);
        var field = { field: column.name, width: column.width };
        function generateSortLink() {
            if (!tableMeta) {
                return undefined;
            }
            var nextEventView = eventView.sortOnField(field, tableMeta);
            var queryStringObject = nextEventView.generateQueryStringObject();
            return tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { sort: queryStringObject.sort }) });
        }
        var currentSort = eventView.sortForField(field, tableMeta);
        // Event id and Trace id are technically sortable but we don't want to sort them here since sorting by a uuid value doesn't make sense
        var canSort = field.field !== 'id' &&
            field.field !== 'trace' &&
            field.field !== fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD &&
            eventView_1.isFieldSortable(field, tableMeta);
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        if (field.field === fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD) {
            title = (<operationSort_1.default title={OperationTitle} eventView={eventView} tableMeta={tableMeta} location={location}/>);
        }
        var sortLink = (<sortLink_1.default align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
        return sortLink;
    };
    EventsTable.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError;
        var widths = this.state.widths;
        var containsSpanOpsBreakdown = eventView
            .getColumns()
            .find(function (col) {
            return col.name === fields_1.SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
        });
        var columnOrder = eventView
            .getColumns()
            .filter(function (col) {
            return !containsSpanOpsBreakdown || !fields_1.isSpanOperationBreakdownField(col.name);
        })
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return tslib_1.__assign(tslib_1.__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        return (<div>
        <discoverQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.transaction-events">
          {function (_a) {
                var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
                return (<React.Fragment>
                <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={eventView.getSorts()} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: _this.renderBodyCellWithData(tableData),
                    }} location={location}/>
                <pagination_1.default pageLinks={pageLinks}/>
              </React.Fragment>);
            }}
        </discoverQuery_1.default>
      </div>);
    };
    return EventsTable;
}(React.Component));
var StyledIconQuestion = styled_1.default(questionTooltip_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"], ["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"])));
exports.default = EventsTable;
var templateObject_1;
//# sourceMappingURL=eventsTable.jsx.map