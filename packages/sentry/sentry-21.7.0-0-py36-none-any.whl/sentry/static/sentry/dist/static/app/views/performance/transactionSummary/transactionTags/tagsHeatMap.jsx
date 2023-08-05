Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var react_popper_1 = require("react-popper");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("@sentry/utils");
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var heatMapChart_1 = tslib_1.__importDefault(require("app/components/charts/heatMapChart"));
var styles_1 = require("app/components/charts/styles");
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var dropdownControl_1 = require("app/components/dropdownControl");
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var styles_2 = require("app/components/quickTrace/styles");
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var charts_1 = require("app/utils/discover/charts");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var tagTransactionsQuery_1 = tslib_1.__importDefault(require("app/utils/performance/segmentExplorer/tagTransactionsQuery"));
var queryString_1 = require("app/utils/queryString");
var utils_2 = require("../../utils");
var utils_3 = require("../transactionEvents/utils");
var utils_4 = require("../utils");
var utils_5 = require("./utils");
var findRowKey = function (row) {
    return Object.keys(row).find(function (key) { return key.includes('histogram'); });
};
var VirtualReference = /** @class */ (function () {
    function VirtualReference(element) {
        this.boundingRect = element.getBoundingClientRect();
    }
    VirtualReference.prototype.getBoundingClientRect = function () {
        return this.boundingRect;
    };
    Object.defineProperty(VirtualReference.prototype, "clientWidth", {
        get: function () {
            return this.getBoundingClientRect().width;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(VirtualReference.prototype, "clientHeight", {
        get: function () {
            return this.getBoundingClientRect().height;
        },
        enumerable: false,
        configurable: true
    });
    return VirtualReference;
}());
var getPortal = memoize_1.default(function () {
    var portal = document.getElementById('heatmap-portal');
    if (!portal) {
        portal = document.createElement('div');
        portal.setAttribute('id', 'heatmap-portal');
        document.body.appendChild(portal);
    }
    return portal;
});
var TagsHeatMap = function (props) {
    var tableData = props.tableData, isLoading = props.isLoading, organization = props.organization, eventView = props.eventView, location = props.location, tagKey = props.tagKey, transactionName = props.transactionName, aggregateColumn = props.aggregateColumn;
    var chartRef = react_1.useRef(null);
    var _a = tslib_1.__read(react_1.useState(), 2), chartElement = _a[0], setChartElement = _a[1];
    var _b = tslib_1.__read(react_1.useState(), 2), transactionEventView = _b[0], setTransactionEventView = _b[1];
    var _c = tslib_1.__read(react_1.useState(false), 2), isMenuOpen = _c[0], setIsMenuOpen = _c[1];
    // TODO(k-fish): Replace with actual theme colors.
    var purples = ['#D1BAFC', '#9282F3', '#6056BA', '#313087', '#021156'];
    var xValues = new Set();
    var histogramData = tableData &&
        tableData.histogram &&
        tableData.histogram.data &&
        tableData.histogram.data.length
        ? tableData.histogram.data
        : undefined;
    var tagData = tableData && tableData.tags && tableData.tags.data ? tableData.tags.data : undefined;
    var rowKey = histogramData && findRowKey(histogramData[0]);
    // Reverse since e-charts takes the axis labels in the opposite order.
    var columnNames = tagData ? tagData.map(function (tag) { return tag.tags_value; }).reverse() : [];
    var maxCount = 0;
    var _data = rowKey && histogramData
        ? histogramData.map(function (row) {
            var rawDuration = row[rowKey];
            var x = utils_2.getPerformanceDuration(rawDuration);
            var y = row.tags_value;
            xValues.add(x);
            maxCount = Math.max(maxCount, row.count);
            return [x, y, row.count];
        })
        : null;
    _data &&
        _data.sort(function (a, b) {
            if (a[0] === b[0]) {
                return b[1] - a[1];
            }
            return b[0] - a[0];
        });
    // TODO(k-fish): Cleanup options
    var chartOptions = {
        height: 290,
        animation: false,
        colors: purples,
        tooltip: {},
        yAxis: {
            type: 'category',
            data: Array.from(columnNames),
            splitArea: {
                show: true,
            },
            axisLabel: {
                formatter: function (value) { return utils_1.truncate(value, 30); },
            },
        },
        xAxis: {
            boundaryGap: true,
            type: 'category',
            splitArea: {
                show: true,
            },
            data: Array.from(xValues),
            axisLabel: {
                show: true,
                showMinLabel: true,
                showMaxLabel: true,
                formatter: function (value) { return charts_1.axisLabelFormatter(value, 'Count'); },
            },
            axisLine: {},
            axisPointer: {
                show: false,
            },
            axisTick: {
                show: true,
                interval: 0,
                alignWithLabel: true,
            },
        },
        grid: {
            left: space_1.default(3),
            right: space_1.default(3),
            top: '25px',
            bottom: space_1.default(4),
        },
    };
    var visualMaps = [
        {
            min: 0,
            max: maxCount,
            show: false,
            orient: 'horizontal',
            calculable: true,
            inRange: {
                color: purples,
            },
        },
    ];
    var series = [];
    if (_data) {
        series.push({
            seriesName: 'Count',
            dataArray: _data,
            label: {
                show: true,
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
            },
        }); // TODO(k-fish): Fix heatmap data typing
    }
    var onOpenMenu = function () {
        setIsMenuOpen(true);
    };
    var onCloseMenu = function () {
        setIsMenuOpen(false);
    };
    var shouldIgnoreMenuClose = function (e) {
        var _a;
        if ((_a = chartRef.current) === null || _a === void 0 ? void 0 : _a.getEchartsInstance().getDom().contains(e.target)) {
            // Ignore the menu being closed if the echart is being clicked.
            return true;
        }
        return false;
    };
    var histogramBucketInfo = histogramData && utils_5.parseHistogramBucketInfo(histogramData[0]);
    return (<StyledPanel>
      <StyledHeaderTitleLegend>
        {locale_1.t('Heat Map')}
        <questionTooltip_1.default size="sm" position="top" title={locale_1.t('This heatmap shows the frequency for each duration across the most common tag values')}/>
      </StyledHeaderTitleLegend>

      <transitionChart_1.default loading={isLoading} reloading={isLoading}>
        <transparentLoadingMask_1.default visible={isLoading}/>
        <dropdownMenu_1.default onOpen={onOpenMenu} onClose={onCloseMenu} shouldIgnoreClickOutside={shouldIgnoreMenuClose}>
          {function (_a) {
            var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, actions = _a.actions;
            var onChartClick = function (bucket) {
                var htmlEvent = bucket.event.event;
                // Make a copy of the dims because echarts can remove elements after this click happens.
                // TODO(k-fish): Look at improving this to respond properly to resize events.
                var virtualRef = new VirtualReference(htmlEvent.target);
                setChartElement(virtualRef);
                var newTransactionEventView = eventView.clone();
                newTransactionEventView.fields = [{ field: aggregateColumn }];
                var _a = tslib_1.__read(bucket.value, 2), _ = _a[0], tagValue = _a[1];
                if (histogramBucketInfo && histogramData) {
                    var row = histogramData[bucket.dataIndex];
                    var currentBucketStart = parseInt("" + row[histogramBucketInfo.histogramField], 10);
                    var currentBucketEnd = currentBucketStart + histogramBucketInfo.bucketSize;
                    newTransactionEventView.additionalConditions.setTagValues(aggregateColumn, [">=" + currentBucketStart, "<" + currentBucketEnd]);
                }
                newTransactionEventView.additionalConditions.setTagValues(tagKey, [
                    tagValue,
                ]);
                setTransactionEventView(newTransactionEventView);
                utils_5.trackTagPageInteraction(organization);
                if (!isMenuOpen) {
                    actions.open();
                }
            };
            return (<react_1.default.Fragment>
                {react_dom_1.default.createPortal(<div>
                    {chartElement ? (<react_popper_1.Popper referenceElement={chartElement} placement="bottom">
                        {function (_a) {
                            var ref = _a.ref, style = _a.style, placement = _a.placement;
                            return (<StyledDropdownContainer ref={ref} style={style} className="anchor-middle" data-placement={placement}>
                            <StyledDropdownContent {...getMenuProps({
                                className: classnames_1.default('dropdown-menu'),
                            })} isOpen={isOpen} alignMenu="right" blendCorner={false}>
                              {transactionEventView ? (<tagTransactionsQuery_1.default query={transactionEventView.getQueryWithAdditionalConditions()} location={location} eventView={transactionEventView} orgSlug={organization.slug} limit={4} referrer="api.performance.tag-page">
                                  {function (_a) {
                                        var isTransactionsLoading = _a.isLoading, transactionTableData = _a.tableData;
                                        var moreEventsTarget = isTransactionsLoading
                                            ? null
                                            : utils_3.eventsRouteWithQuery({
                                                orgSlug: organization.slug,
                                                transaction: transactionName,
                                                projectID: queryString_1.decodeScalar(location.query.project),
                                                query: tslib_1.__assign(tslib_1.__assign({}, transactionEventView.generateQueryStringObject()), { query: transactionEventView.getQueryWithAdditionalConditions() }),
                                            });
                                        return (<react_1.default.Fragment>
                                        {isTransactionsLoading ? (<LoadingContainer>
                                            <loadingIndicator_1.default size={40} hideMessage/>
                                          </LoadingContainer>) : (<div>
                                            {!transactionTableData.data.length ? (<placeholder_1.default />) : null}
                                            {tslib_1.__spreadArray([], tslib_1.__read(transactionTableData.data)).slice(0, 3)
                                                    .map(function (row) {
                                                    var target = utils_4.generateTransactionLink(transactionName)(organization, row, location.query);
                                                    return (<styles_2.DropdownItem width="small" key={row.id} to={target}>
                                                    <DropdownItemContainer>
                                                      <truncate_1.default value={row.id} maxLength={12}/>
                                                      <styles_2.SectionSubtext>
                                                        <utils_2.PerformanceDuration milliseconds={row[aggregateColumn]} abbreviation/>
                                                      </styles_2.SectionSubtext>
                                                    </DropdownItemContainer>
                                                  </styles_2.DropdownItem>);
                                                })}
                                            {moreEventsTarget &&
                                                    transactionTableData.data.length > 3 ? (<styles_2.DropdownItem width="small" to={moreEventsTarget}>
                                                <DropdownItemContainer>
                                                  {locale_1.t('View all events')}
                                                </DropdownItemContainer>
                                              </styles_2.DropdownItem>) : null}
                                          </div>)}
                                      </react_1.default.Fragment>);
                                    }}
                                </tagTransactionsQuery_1.default>) : null}
                            </StyledDropdownContent>
                          </StyledDropdownContainer>);
                        }}
                      </react_popper_1.Popper>) : null}
                  </div>, getPortal())}

                {getDynamicText_1.default({
                    value: (<heatMapChart_1.default ref={chartRef} visualMaps={visualMaps} series={series} onClick={onChartClick} {...chartOptions}/>),
                    fixed: <placeholder_1.default height="290px" testId="skeleton-ui"/>,
                })}
              </react_1.default.Fragment>);
        }}
        </dropdownMenu_1.default>
      </transitionChart_1.default>
    </StyledPanel>);
};
var LoadingContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 200px;\n  height: 100px;\n\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: 200px;\n  height: 100px;\n\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var DropdownItemContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  flex-direction: row;\n\n  justify-content: space-between;\n"], ["\n  width: 100%;\n  display: flex;\n  flex-direction: row;\n\n  justify-content: space-between;\n"])));
var StyledDropdownContainer = styled_1.default(styles_2.DropdownContainer)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.dropdown; });
var StyledDropdownContent = styled_1.default(dropdownControl_1.Content)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  right: auto;\n  transform: translate(-50%);\n\n  overflow: visible;\n"], ["\n  right: auto;\n  transform: translate(-50%);\n\n  overflow: visible;\n"])));
var StyledPanel = styled_1.default(panels_1.Panel)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", " 0 ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  padding: ", " ", " 0 ", ";\n  margin-bottom: 0;\n  border-bottom: 0;\n  border-bottom-left-radius: 0;\n  border-bottom-right-radius: 0;\n"])), space_1.default(3), space_1.default(3), space_1.default(3));
var StyledHeaderTitleLegend = styled_1.default(styles_1.HeaderTitleLegend)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject([""], [""])));
exports.default = react_2.withTheme(TagsHeatMap);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=tagsHeatMap.jsx.map