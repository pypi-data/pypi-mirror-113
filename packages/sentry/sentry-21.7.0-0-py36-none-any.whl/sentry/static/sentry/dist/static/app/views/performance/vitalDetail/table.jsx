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
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var vitalsDetailsTableQuery_1 = tslib_1.__importDefault(require("app/utils/performance/vitals/vitalsDetailsTableQuery"));
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = tslib_1.__importStar(require("app/views/eventsV2/table/cellAction"));
var charts_1 = require("../transactionSummary/charts");
var utils_1 = require("../transactionSummary/utils");
var utils_2 = require("./utils");
var COLUMN_TITLES = ['Transaction', 'Project', 'Unique Users', 'Count'];
var getTableColumnTitle = function (index, vitalName) {
    var abbrev = utils_2.vitalAbbreviations[vitalName];
    var titles = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(COLUMN_TITLES)), [
        "p50(" + abbrev + ")",
        "p75(" + abbrev + ")",
        "p95(" + abbrev + ")",
        "Status",
    ]);
    return titles[index];
};
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
var Table = /** @class */ (function (_super) {
    tslib_1.__extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
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
        _this.renderBodyCellWithData = function (tableData, vitalName) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow, vitalName); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta, vitalName) {
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, getTableColumnTitle(index, vitalName));
            };
        };
        _this.renderPrependCellWithData = function (tableData, vitalName) {
            var eventView = _this.props.eventView;
            var keyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'key_transaction'; });
            var teamKeyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'team_key_transaction'; });
            return function (isHeader, dataRow) {
                if (keyTransactionColumn) {
                    if (isHeader) {
                        var star = (<icons_1.IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                        return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, keyTransactionColumn, star)];
                    }
                    else {
                        return [
                            _this.renderBodyCell(tableData, keyTransactionColumn, dataRow, vitalName),
                        ];
                    }
                }
                else if (teamKeyTransactionColumn) {
                    if (isHeader) {
                        var star = (<icons_1.IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                        return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, teamKeyTransactionColumn, star)];
                    }
                    else {
                        return [
                            _this.renderBodyCell(tableData, teamKeyTransactionColumn, dataRow, vitalName),
                        ];
                    }
                }
                return [];
            };
        };
        _this.handleSummaryClick = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
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
    Table.prototype.renderBodyCell = function (tableData, column, dataRow, vitalName) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location, summaryConditions = _a.summaryConditions;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        if (field === utils_2.getVitalDetailTablePoorStatusFunction(vitalName)) {
            if (dataRow[fields_1.getAggregateAlias(field)]) {
                return (<UniqueTagCell>
            <PoorTag>{locale_1.t('Poor')}</PoorTag>
          </UniqueTagCell>);
            }
            else if (dataRow[fields_1.getAggregateAlias(utils_2.getVitalDetailTableMehStatusFunction(vitalName))]) {
                return (<UniqueTagCell>
            <MehTag>{locale_1.t('Meh')}</MehTag>
          </UniqueTagCell>);
            }
            else {
                return (<UniqueTagCell>
            <GoodTag>{locale_1.t('Good')}</GoodTag>
          </UniqueTagCell>);
            }
        }
        var fieldRenderer = fieldRenderers_1.getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        var allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
        ];
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            var conditions = tokenizeSearch_1.tokenizeSearch(summaryConditions);
            conditions.addTagValues('has', ["" + vitalName]);
            summaryView.query = conditions.formatString();
            var target = utils_1.transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
                showTransactions: utils_1.TransactionFilterOptions.RECENT,
                display: charts_1.DisplayModes.VITALS,
            });
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <link_1.default to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </link_1.default>
        </cellAction_1.default>);
        }
        if (field.startsWith('key_transaction')) {
            return rendered;
        }
        if (field.startsWith('team_key_transaction')) {
            return rendered;
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
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
        var canSort = eventView_1.isFieldSortable(field, tableMeta);
        return (<sortLink_1.default align={align} title={title || field.field} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
    };
    Table.prototype.getSortedEventView = function (vitalName) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        var aggregateFieldPoor = fields_1.getAggregateAlias(utils_2.getVitalDetailTablePoorStatusFunction(vitalName));
        var aggregateFieldMeh = fields_1.getAggregateAlias(utils_2.getVitalDetailTableMehStatusFunction(vitalName));
        var isSortingByStatus = eventView.sorts.some(function (sort) {
            return sort.field.includes(aggregateFieldPoor) || sort.field.includes(aggregateFieldMeh);
        });
        var additionalSorts = isSortingByStatus
            ? []
            : [
                {
                    field: organization.features.includes('team-key-transactions')
                        ? 'team_key_transaction'
                        : 'key_transaction',
                    kind: 'desc',
                },
                {
                    field: aggregateFieldPoor,
                    kind: 'desc',
                },
                {
                    field: aggregateFieldMeh,
                    kind: 'desc',
                },
            ];
        return eventView.withSorts(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(additionalSorts)), tslib_1.__read(eventView.sorts)));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var widths = this.state.widths;
        var fakeColumnView = eventView.clone();
        fakeColumnView.fields = tslib_1.__spreadArray([], tslib_1.__read(eventView.fields));
        var columnOrder = fakeColumnView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter(function (col) {
            return col.name !== 'key_transaction' && col.name !== 'team_key_transaction';
        })
            .slice(0, -1)
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return tslib_1.__assign(tslib_1.__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var vitalName = utils_2.vitalNameFromLocation(location);
        var sortedEventView = this.getSortedEventView(vitalName);
        var columnSortBy = sortedEventView.getSorts();
        return (<div>
        <vitalsDetailsTableQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} limit={10} referrer="api.performance.vital-detail">
          {function (_a) {
                var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
                return (<React.Fragment>
              <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta, vitalName),
                        renderBodyCell: _this.renderBodyCellWithData(tableData, vitalName),
                        renderPrependColumns: _this.renderPrependCellWithData(tableData, vitalName),
                        prependColumnWidths: ['max-content'],
                    }} location={location}/>
              <pagination_1.default pageLinks={pageLinks}/>
            </React.Fragment>);
            }}
        </vitalsDetailsTableQuery_1.default>
      </div>);
    };
    return Table;
}(React.Component));
var UniqueTagCell = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var GoodTag = styled_1.default(tag_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), function (p) { return p.theme[utils_2.vitalStateColors[utils_2.VitalState.GOOD]]; }, function (p) { return p.theme.white; });
var MehTag = styled_1.default(tag_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), function (p) { return p.theme[utils_2.vitalStateColors[utils_2.VitalState.MEH]]; }, function (p) { return p.theme.white; });
var PoorTag = styled_1.default(tag_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), function (p) { return p.theme[utils_2.vitalStateColors[utils_2.VitalState.POOR]]; }, function (p) { return p.theme.white; });
exports.default = Table;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=table.jsx.map