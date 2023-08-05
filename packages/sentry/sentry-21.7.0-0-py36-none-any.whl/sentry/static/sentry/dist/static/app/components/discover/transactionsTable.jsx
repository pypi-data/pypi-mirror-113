Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var sortLink_1 = tslib_1.__importDefault(require("app/components/gridEditable/sortLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panelTable_1 = tslib_1.__importDefault(require("app/components/panels/panelTable"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var urls_1 = require("app/utils/discover/urls");
var formatters_1 = require("app/utils/formatters");
var cellAction_1 = tslib_1.__importDefault(require("app/views/eventsV2/table/cellAction"));
var styles_1 = require("app/views/performance/styles");
var utils_1 = require("app/views/performance/utils");
var TransactionsTable = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionsTable, _super);
    function TransactionsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionsTable.prototype.getTitles = function () {
        var _a = this.props, eventView = _a.eventView, titles = _a.titles;
        return titles !== null && titles !== void 0 ? titles : eventView.getFields();
    };
    TransactionsTable.prototype.renderHeader = function () {
        var _a = this.props, tableData = _a.tableData, columnOrder = _a.columnOrder, baselineTransactionName = _a.baselineTransactionName;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var generateSortLink = function () { return undefined; };
        var tableTitles = this.getTitles();
        var headers = tableTitles.map(function (title, index) {
            var column = columnOrder[index];
            var align = fields_1.fieldAlignment(column.name, column.type, tableMeta);
            if (column.key === 'span_ops_breakdown.relative') {
                return (<HeadCellContainer key={index}>
            <guideAnchor_1.default target="span_op_relative_breakdowns">
              <sortLink_1.default align={align} title={title === locale_1.t('operation duration') ? (<React.Fragment>
                      {title}
                      <StyledIconQuestion size="xs" position="top" title={locale_1.t("Span durations are summed over the course of an entire transaction. Any overlapping spans are only counted once.")}/>
                    </React.Fragment>) : (title)} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </guideAnchor_1.default>
          </HeadCellContainer>);
            }
            return (<HeadCellContainer key={index}>
          <sortLink_1.default align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        });
        if (baselineTransactionName) {
            headers.push(<HeadCellContainer key="baseline">
          <sortLink_1.default align="right" title={locale_1.t('Compared to Baseline')} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        }
        return headers;
    };
    TransactionsTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, generateLink = _a.generateLink, baselineTransactionName = _a.baselineTransactionName, baselineData = _a.baselineData, handleBaselineClick = _a.handleBaselineClick, handleCellAction = _a.handleCellAction, titles = _a.titles;
        var fields = eventView.getFields();
        if (titles && titles.length) {
            // Slice to match length of given titles
            columnOrder = columnOrder.slice(0, titles.length);
        }
        var resultsRow = columnOrder.map(function (column, index) {
            var _a;
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = fields_1.getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = fieldRenderers_1.getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            var target = (_a = generateLink === null || generateLink === void 0 ? void 0 : generateLink[field]) === null || _a === void 0 ? void 0 : _a.call(generateLink, organization, row, location.query);
            if (target) {
                rendered = (<link_1.default data-test-id={"view-" + fields[index]} to={target}>
            {rendered}
          </link_1.default>);
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            rendered = isNumeric ? (<styles_1.GridCellNumber>{rendered}</styles_1.GridCellNumber>) : (<styles_1.GridCell>{rendered}</styles_1.GridCell>);
            if (handleCellAction) {
                rendered = (<cellAction_1.default column={column} dataRow={row} handleCellAction={handleCellAction(column)}>
            {rendered}
          </cellAction_1.default>);
            }
            return <BodyCellContainer key={key}>{rendered}</BodyCellContainer>;
        });
        if (baselineTransactionName) {
            if (baselineData) {
                var currentTransactionDuration = Number(row['transaction.duration']) || 0;
                var duration = baselineData['transaction.duration'];
                var delta = Math.abs(currentTransactionDuration - duration);
                var relativeSpeed = currentTransactionDuration < duration
                    ? locale_1.t('faster')
                    : currentTransactionDuration > duration
                        ? locale_1.t('slower')
                        : '';
                var target = utils_1.getTransactionComparisonUrl({
                    organization: organization,
                    baselineEventSlug: urls_1.generateEventSlug(baselineData),
                    regressionEventSlug: urls_1.generateEventSlug(row),
                    transaction: baselineTransactionName,
                    query: location.query,
                });
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"} style={{ textAlign: 'right' }}>
            <styles_1.GridCell>
              <link_1.default to={target} onClick={handleBaselineClick}>
                {formatters_1.getDuration(delta / 1000, delta < 1000 ? 0 : 2) + " " + relativeSpeed}
              </link_1.default>
            </styles_1.GridCell>
          </BodyCellContainer>);
            }
            else {
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"}>
            {'\u2014'}
          </BodyCellContainer>);
            }
        }
        return resultsRow;
    };
    TransactionsTable.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData, columnOrder = _a.columnOrder;
        var cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        tableData.data.forEach(function (row, i) {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(_this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    };
    TransactionsTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        var loader = <loadingIndicator_1.default style={{ margin: '70px auto' }}/>;
        return (<panelTable_1.default isEmpty={!hasResults} emptyMessage={locale_1.t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </panelTable_1.default>);
    };
    return TransactionsTable;
}(React.PureComponent));
var HeadCellContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(2));
var BodyCellContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  ", ";\n"], ["\n  padding: ", " ", ";\n  ", ";\n"])), space_1.default(1), space_1.default(2), overflowEllipsis_1.default);
var StyledIconQuestion = styled_1.default(questionTooltip_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"], ["\n  position: relative;\n  top: 1px;\n  left: 4px;\n"])));
exports.default = TransactionsTable;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionsTable.jsx.map