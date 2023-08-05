Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var modal_1 = require("app/actionCreators/modal");
var gridEditable_1 = tslib_1.__importStar(require("app/components/gridEditable"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var types_1 = require("app/utils/discover/types");
var urls_1 = require("app/utils/discover/urls");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var utils_2 = require("app/views/performance/traceDetails/utils");
var utils_3 = require("app/views/performance/transactionSummary/utils");
var utils_4 = require("../utils");
var cellAction_1 = tslib_1.__importStar(require("./cellAction"));
var columnEditModal_1 = tslib_1.__importStar(require("./columnEditModal"));
var tableActions_1 = tslib_1.__importDefault(require("./tableActions"));
/**
 * The `TableView` is marked with leading _ in its method names. It consumes
 * the EventView object given in its props to generate new EventView objects
 * for actions like resizing column.

 * The entire state of the table view (or event view) is co-located within
 * the EventView object. This object is fed from the props.
 *
 * Attempting to modify the state, and therefore, modifying the given EventView
 * object given from its props, will generate new instances of EventView objects.
 *
 * In most cases, the new EventView object differs from the previous EventView
 * object. The new EventView object is pushed to the location object.
 */
var TableView = /** @class */ (function (_super) {
    tslib_1.__extends(TableView, _super);
    function TableView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Updates a column on resizing
         */
        _this._resizeColumn = function (columnIndex, nextColumn) {
            var _a = _this.props, location = _a.location, eventView = _a.eventView;
            var newWidth = nextColumn.width ? Number(nextColumn.width) : gridEditable_1.COL_WIDTH_UNDEFINED;
            var nextEventView = eventView.withResizedColumn(columnIndex, newWidth);
            utils_4.pushEventViewToLocation({
                location: location,
                nextEventView: nextEventView,
                extraQuery: eventView_1.pickRelevantLocationQueryStrings(location),
            });
        };
        _this._renderPrependColumns = function (isHeader, dataRow, rowIndex) {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, tableData = _a.tableData, location = _a.location;
            var hasAggregates = eventView.hasAggregateField();
            var hasIdField = eventView.hasIdField();
            if (isHeader) {
                if (hasAggregates) {
                    return [
                        <PrependHeader key="header-icon">
            <icons_1.IconStack size="sm"/>
          </PrependHeader>,
                    ];
                }
                else if (!hasIdField) {
                    return [
                        <PrependHeader key="header-event-id">
            <sortLink_1.default align="left" title={locale_1.t('event id')} direction={undefined} canSort={false} generateSortLink={function () { return undefined; }}/>
          </PrependHeader>,
                    ];
                }
                else {
                    return [];
                }
            }
            if (hasAggregates) {
                var nextView_1 = utils_4.getExpandedResults(eventView, {}, dataRow);
                var target = {
                    pathname: location.pathname,
                    query: nextView_1.generateQueryStringObject(),
                };
                return [
                    <tooltip_1.default key={"eventlink" + rowIndex} title={locale_1.t('Open Group')}>
          <link_1.default to={target} data-test-id="open-group" onClick={function () {
                            if (nextView_1.isEqualTo(eventView)) {
                                Sentry.captureException(new Error('Failed to drilldown'));
                            }
                        }}>
            <StyledIcon size="sm"/>
          </link_1.default>
        </tooltip_1.default>,
                ];
            }
            else if (!hasIdField) {
                var value = dataRow.id;
                if (tableData && tableData.meta) {
                    var fieldRenderer = fieldRenderers_1.getFieldRenderer('id', tableData.meta);
                    value = fieldRenderer(dataRow, { organization: organization, location: location });
                }
                var eventSlug = urls_1.generateEventSlug(dataRow);
                var target = urls_1.eventDetailsRouteWithEventView({
                    orgSlug: organization.slug,
                    eventSlug: eventSlug,
                    eventView: eventView,
                });
                return [
                    <tooltip_1.default key={"eventlink" + rowIndex} title={locale_1.t('View Event')}>
          <StyledLink data-test-id="view-event" to={target}>
            {value}
          </StyledLink>
        </tooltip_1.default>,
                ];
            }
            else {
                return [];
            }
        };
        _this._renderGridHeaderCell = function (column) {
            var _a = _this.props, eventView = _a.eventView, location = _a.location, tableData = _a.tableData;
            var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
            var align = fields_1.fieldAlignment(column.name, column.type, tableMeta);
            var field = { field: column.name, width: column.width };
            function generateSortLink() {
                if (!tableMeta) {
                    return undefined;
                }
                var nextEventView = eventView.sortOnField(field, tableMeta);
                var queryStringObject = nextEventView.generateQueryStringObject();
                return tslib_1.__assign(tslib_1.__assign({}, location), { query: queryStringObject });
            }
            var currentSort = eventView.sortForField(field, tableMeta);
            var canSort = eventView_1.isFieldSortable(field, tableMeta);
            var titleText = fields_1.isEquationAlias(column.name)
                ? eventView.getEquations()[fields_1.getEquationAliasIndex(column.name)]
                : column.name;
            var title = (<StyledTooltip title={titleText}>
        <truncate_1.default value={titleText} maxLength={60} expandable={false}/>
      </StyledTooltip>);
            return (<sortLink_1.default align={align} title={title} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
        };
        _this._renderGridBodyCell = function (column, dataRow, rowIndex, columnIndex) {
            var _a, _b;
            var _c = _this.props, isFirstPage = _c.isFirstPage, eventView = _c.eventView, location = _c.location, organization = _c.organization, tableData = _c.tableData;
            if (!tableData || !tableData.meta) {
                return dataRow[column.key];
            }
            var columnKey = String(column.key);
            var fieldRenderer = fieldRenderers_1.getFieldRenderer(columnKey, tableData.meta);
            var display = eventView.getDisplayMode();
            var isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
            var count = Math.min((_b = (_a = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : types_1.TOP_N, types_1.TOP_N);
            var cell = fieldRenderer(dataRow, { organization: organization, location: location });
            if (columnKey === 'id') {
                var eventSlug = urls_1.generateEventSlug(dataRow);
                var target = urls_1.eventDetailsRouteWithEventView({
                    orgSlug: organization.slug,
                    eventSlug: eventSlug,
                    eventView: eventView,
                });
                cell = (<tooltip_1.default title={locale_1.t('View Event')}>
          <StyledLink data-test-id="view-event" to={target}>
            {cell}
          </StyledLink>
        </tooltip_1.default>);
            }
            else if (columnKey === 'trace') {
                var dateSelection = eventView.normalizeDateSelection(location);
                if (dataRow.trace) {
                    var target = utils_2.getTraceDetailsUrl(organization, String(dataRow.trace), dateSelection, {});
                    cell = (<tooltip_1.default title={locale_1.t('View Trace')}>
            <StyledLink data-test-id="view-trace" to={target}>
              {cell}
            </StyledLink>
          </tooltip_1.default>);
                }
            }
            var fieldName = fields_1.getAggregateAlias(columnKey);
            var value = dataRow[fieldName];
            if (tableData.meta[fieldName] === 'integer' && utils_1.defined(value) && value > 999) {
                return (<tooltip_1.default title={value.toLocaleString()} containerDisplayMode="block" position="right">
          <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={_this.handleCellAction(dataRow, column)}>
            {cell}
          </cellAction_1.default>
        </tooltip_1.default>);
            }
            return (<React.Fragment>
        {isFirstPage && isTopEvents && rowIndex < types_1.TOP_N && columnIndex === 0 ? (<TopResultsIndicator count={count} index={rowIndex}/>) : null}
        <cellAction_1.default column={column} dataRow={dataRow} handleCellAction={_this.handleCellAction(dataRow, column)}>
          {cell}
        </cellAction_1.default>
      </React.Fragment>);
        };
        _this.handleEditColumns = function () {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, tagKeys = _a.tagKeys, measurementKeys = _a.measurementKeys, spanOperationBreakdownKeys = _a.spanOperationBreakdownKeys;
            var hasBreakdownFeature = organization.features.includes('performance-ops-breakdown');
            modal_1.openModal(function (modalProps) { return (<columnEditModal_1.default {...modalProps} organization={organization} tagKeys={tagKeys} measurementKeys={measurementKeys} spanOperationBreakdownKeys={hasBreakdownFeature ? spanOperationBreakdownKeys : undefined} columns={eventView.getColumns().map(function (col) { return col.column; })} onApply={_this.handleUpdateColumns}/>); }, { modalCss: columnEditModal_1.modalCss, backdrop: 'static' });
        };
        _this.handleCellAction = function (dataRow, column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
                var query = tokenizeSearch_1.tokenizeSearch(eventView.query);
                var nextView = eventView.clone();
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'discover_v2.results.cellaction',
                    eventName: 'Discoverv2: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                switch (action) {
                    case cellAction_1.Actions.TRANSACTION: {
                        var maybeProject = projects.find(function (project) { return project.slug === dataRow.project; });
                        var projectID = maybeProject ? [maybeProject.id] : undefined;
                        var next = utils_3.transactionSummaryRouteWithQuery({
                            orgSlug: organization.slug,
                            transaction: String(value),
                            projectID: projectID,
                            query: nextView.getGlobalSelectionQuery(),
                        });
                        react_router_1.browserHistory.push(next);
                        return;
                    }
                    case cellAction_1.Actions.RELEASE: {
                        var maybeProject = projects.find(function (project) {
                            return project.slug === dataRow.project;
                        });
                        react_router_1.browserHistory.push({
                            pathname: "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(value) + "/",
                            query: tslib_1.__assign(tslib_1.__assign({}, nextView.getGlobalSelectionQuery()), { project: maybeProject ? maybeProject.id : undefined }),
                        });
                        return;
                    }
                    case cellAction_1.Actions.DRILLDOWN: {
                        // count_unique(column) drilldown
                        analytics_1.trackAnalyticsEvent({
                            eventKey: 'discover_v2.results.drilldown',
                            eventName: 'Discoverv2: Click aggregate drilldown',
                            organization_id: parseInt(organization.id, 10),
                        });
                        // Drilldown into each distinct value and get a count() for each value.
                        nextView = utils_4.getExpandedResults(nextView, {}, dataRow).withNewColumn({
                            kind: 'function',
                            function: ['count', '', undefined, undefined],
                        });
                        react_router_1.browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
                        return;
                    }
                    default: {
                        cellAction_1.updateQuery(query, action, column, value);
                    }
                }
                nextView.query = query.formatString();
                react_router_1.browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
            };
        };
        _this.handleUpdateColumns = function (columns) {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView;
            // metrics
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.update_columns',
                eventName: 'Discoverv2: Update columns',
                organization_id: parseInt(organization.id, 10),
            });
            var nextView = eventView.withColumns(columns);
            react_router_1.browserHistory.push(nextView.getResultsViewUrlTarget(organization.slug));
        };
        _this.renderHeaderButtons = function () {
            var _a = _this.props, organization = _a.organization, title = _a.title, eventView = _a.eventView, isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData, location = _a.location, onChangeShowTags = _a.onChangeShowTags, showTags = _a.showTags;
            return (<tableActions_1.default title={title} isLoading={isLoading} error={error} organization={organization} eventView={eventView} onEdit={_this.handleEditColumns} tableData={tableData} location={location} onChangeShowTags={onChangeShowTags} showTags={showTags}/>);
        };
        return _this;
    }
    TableView.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, error = _a.error, location = _a.location, tableData = _a.tableData, eventView = _a.eventView;
        var columnOrder = eventView.getColumns();
        var columnSortBy = eventView.getSorts();
        var prependColumnWidths = eventView.hasAggregateField()
            ? ['40px']
            : eventView.hasIdField()
                ? []
                : ["minmax(" + gridEditable_1.COL_WIDTH_MINIMUM + "px, max-content)"];
        return (<gridEditable_1.default isLoading={isLoading} error={error} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} title={locale_1.t('Results')} grid={{
                renderHeadCell: this._renderGridHeaderCell,
                renderBodyCell: this._renderGridBodyCell,
                onResizeColumn: this._resizeColumn,
                renderPrependColumns: this._renderPrependColumns,
                prependColumnWidths: prependColumnWidths,
            }} headerButtons={this.renderHeaderButtons} location={location}/>);
    };
    return TableView;
}(React.Component));
var PrependHeader = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledTooltip = styled_1.default(tooltip_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: initial;\n"], ["\n  display: initial;\n"])));
var StyledLink = styled_1.default(link_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  > div {\n    display: inline;\n  }\n"], ["\n  > div {\n    display: inline;\n  }\n"])));
var StyledIcon = styled_1.default(icons_1.IconStack)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  vertical-align: middle;\n"], ["\n  vertical-align: middle;\n"])));
var TopResultsIndicator = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  left: -1px;\n  margin-top: 4.5px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ", ";\n"], ["\n  position: absolute;\n  left: -1px;\n  margin-top: 4.5px;\n  width: 9px;\n  height: 15px;\n  border-radius: 0 3px 3px 0;\n\n  background-color: ", ";\n"])), function (p) {
    // this background color needs to match the colors used in
    // app/components/charts/eventsChart so that the ordering matches
    // the color pallete contains n + 2 colors, so we subtract 2 here
    return p.theme.charts.getColorPalette(p.count - 2)[p.index];
});
exports.default = withProjects_1.default(TableView);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=tableView.jsx.map