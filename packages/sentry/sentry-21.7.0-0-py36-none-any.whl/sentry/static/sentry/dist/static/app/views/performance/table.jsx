Object.defineProperty(exports, "__esModule", { value: true });
exports.getProjectID = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var performance_1 = require("app/actionCreators/performance");
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var gridEditable_1 = tslib_1.__importStar(require("app/components/gridEditable"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var eventView_1 = require("app/utils/discover/eventView");
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var cellAction_1 = tslib_1.__importStar(require("app/views/eventsV2/table/cellAction"));
var transactionThresholdModal_1 = tslib_1.__importStar(require("./transactionSummary/transactionThresholdModal"));
var utils_2 = require("./transactionSummary/utils");
var data_1 = require("./data");
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
            keyedTransactions: null,
            transaction: undefined,
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
        };
        _this.handleCellAction = function (column, dataRow) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization, projects = _a.projects;
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                if (action === cellAction_1.Actions.EDIT_THRESHOLD) {
                    var project_threshold_1 = dataRow.project_threshold_config;
                    var transactionName_1 = dataRow.transaction;
                    var projectID_1 = getProjectID(dataRow, projects);
                    modal_1.openModal(function (modalProps) { return (<transactionThresholdModal_1.default {...modalProps} organization={organization} transactionName={transactionName_1} eventView={eventView} project={projectID_1} transactionThreshold={project_threshold_1[1]} transactionThresholdMetric={project_threshold_1[0]} onApply={function (threshold, metric) {
                            if (threshold !== project_threshold_1[1] ||
                                metric !== project_threshold_1[0]) {
                                _this.setState({
                                    transaction: transactionName_1,
                                    transactionThreshold: threshold,
                                    transactionThresholdMetric: metric,
                                });
                            }
                            indicator_1.addSuccessMessage(locale_1.tct('[transactionName] updated successfully', {
                                transactionName: transactionName_1,
                            }));
                        }}/>); }, { modalCss: transactionThresholdModal_1.modalCss, backdrop: 'static' });
                    return;
                }
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
        _this.renderPrependCellWithData = function (tableData) {
            var eventView = _this.props.eventView;
            var keyedTransactions = _this.state.keyedTransactions;
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
                        return [_this.renderBodyCell(tableData, keyTransactionColumn, dataRow)];
                    }
                }
                else if (teamKeyTransactionColumn) {
                    if (isHeader) {
                        var star = (<guideAnchor_1.default target="team_key_transaction_header" position="top" disabled={keyedTransactions === null} // wait for the legacy counts to load
                        >
              <guideAnchor_1.default target="team_key_transaction_existing" position="top" disabled={!keyedTransactions}>
                <icons_1.IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="team-key-transaction-header"/>
              </guideAnchor_1.default>
            </guideAnchor_1.default>);
                        return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, teamKeyTransactionColumn, star)];
                    }
                    else {
                        return [_this.renderBodyCell(tableData, teamKeyTransactionColumn, dataRow)];
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
    Table.prototype.componentDidMount = function () {
        this.fetchKeyTransactionCount();
    };
    Table.prototype.fetchKeyTransactionCount = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var organization, count, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        organization = this.props.organization;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, performance_1.fetchLegacyKeyTransactionsCount(organization.slug)];
                    case 2:
                        count = _a.sent();
                        this.setState({ keyedTransactions: count });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        this.setState({ keyedTransactions: null });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Table.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = fieldRenderers_1.getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        var allowActions = [
            cellAction_1.Actions.ADD,
            cellAction_1.Actions.EXCLUDE,
            cellAction_1.Actions.SHOW_GREATER_THAN,
            cellAction_1.Actions.SHOW_LESS_THAN,
        ];
        if (organization.features.includes('project-transaction-threshold-override')) {
            allowActions.push(cellAction_1.Actions.EDIT_THRESHOLD);
        }
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            if (dataRow['http.method']) {
                summaryView.additionalConditions.setTagValues('http.method', [
                    dataRow['http.method'],
                ]);
            }
            summaryView.query = summaryView.getQueryWithAdditionalConditions();
            var target = utils_2.transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
            });
            return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
          <link_1.default to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </link_1.default>
        </cellAction_1.default>);
        }
        if (field.startsWith('key_transaction')) {
            // don't display per cell actions for key_transaction
            return rendered;
        }
        if (field.startsWith('team_key_transaction')) {
            // don't display per cell actions for team_key_transaction
            return rendered;
        }
        var fieldName = fields_1.getAggregateAlias(field);
        var value = dataRow[fieldName];
        if (tableMeta[fieldName] === 'integer' && utils_1.defined(value) && value > 999) {
            return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
            {rendered}
          </cellAction_1.default>
        </tooltip_1.default>);
        }
        return (<cellAction_1.default column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column, dataRow)} allowActions={allowActions}>
        {rendered}
      </cellAction_1.default>);
    };
    Table.prototype.onSortClick = function (currentSortKind, currentSortField) {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.landingv2.transactions.sort',
            eventName: 'Performance Views: Landing Transactions Sorted',
            organization_id: parseInt(organization.id, 10),
            field: currentSortField,
            direction: currentSortKind,
        });
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
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
        var currentSortKind = currentSort ? currentSort.kind : undefined;
        var currentSortField = currentSort ? currentSort.field : undefined;
        var sortLink = (<sortLink_1.default align={align} title={title || field.field} direction={currentSortKind} canSort={canSort} generateSortLink={generateSortLink} onClick={function () { return _this.onSortClick(currentSortKind, currentSortField); }}/>);
        if (field.field.startsWith('user_misery')) {
            return (<guideAnchor_1.default target="project_transaction_threshold" position="top" disabled={!organization.features.includes('project-transaction-threshold')}>
          {sortLink}
        </guideAnchor_1.default>);
        }
        return sortLink;
    };
    Table.prototype.getSortedEventView = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        return eventView.withSorts(tslib_1.__spreadArray([
            {
                field: organization.features.includes('team-key-transactions')
                    ? 'team_key_transaction'
                    : 'key_transaction',
                kind: 'desc',
            }
        ], tslib_1.__read(eventView.sorts)));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, setError = _a.setError;
        var _b = this.state, widths = _b.widths, transaction = _b.transaction, transactionThreshold = _b.transactionThreshold, transactionThresholdMetric = _b.transactionThresholdMetric;
        var columnOrder = eventView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter(function (col) {
            return col.name !== 'key_transaction' &&
                col.name !== 'team_key_transaction' &&
                !col.name.startsWith('count_miserable') &&
                col.name !== 'project_threshold_config';
        })
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return tslib_1.__assign(tslib_1.__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var sortedEventView = this.getSortedEventView();
        var columnSortBy = sortedEventView.getSorts();
        var prependColumnWidths = ['max-content'];
        return (<div>
        <discoverQuery_1.default eventView={sortedEventView} orgSlug={organization.slug} location={location} setError={setError} referrer="api.performance.landing-table" transactionName={transaction} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric}>
          {function (_a) {
                var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
                return (<React.Fragment>
              <gridEditable_1.default isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: _this.renderBodyCellWithData(tableData),
                        renderPrependColumns: _this.renderPrependCellWithData(tableData),
                        prependColumnWidths: prependColumnWidths,
                    }} location={location}/>
              <pagination_1.default pageLinks={pageLinks}/>
            </React.Fragment>);
            }}
        </discoverQuery_1.default>
      </div>);
    };
    return Table;
}(React.Component));
exports.default = Table;
//# sourceMappingURL=table.jsx.map