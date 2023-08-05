Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var areaChart_1 = tslib_1.__importDefault(require("app/components/charts/areaChart"));
var barChart_1 = tslib_1.__importDefault(require("app/components/charts/barChart"));
var chartZoom_1 = tslib_1.__importDefault(require("app/components/charts/chartZoom"));
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var lineChart_1 = tslib_1.__importDefault(require("app/components/charts/lineChart"));
var simpleTableChart_1 = tslib_1.__importDefault(require("app/components/charts/simpleTableChart"));
var transitionChart_1 = tslib_1.__importDefault(require("app/components/charts/transitionChart"));
var transparentLoadingMask_1 = tslib_1.__importDefault(require("app/components/charts/transparentLoadingMask"));
var utils_1 = require("app/components/charts/utils");
var worldMapChart_1 = tslib_1.__importDefault(require("app/components/charts/worldMapChart"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var charts_1 = require("app/utils/discover/charts");
var fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
var fields_1 = require("app/utils/discover/fields");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var WidgetCardChart = /** @class */ (function (_super) {
    tslib_1.__extends(WidgetCardChart, _super);
    function WidgetCardChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCardChart.prototype.shouldComponentUpdate = function (nextProps) {
        // Widget title changes should not update the WidgetCardChart component tree
        var currentProps = tslib_1.__assign(tslib_1.__assign({}, this.props), { widget: tslib_1.__assign(tslib_1.__assign({}, this.props.widget), { title: '' }) });
        nextProps = tslib_1.__assign(tslib_1.__assign({}, nextProps), { widget: tslib_1.__assign(tslib_1.__assign({}, nextProps.widget), { title: '' }) });
        return !isEqual_1.default(currentProps, nextProps);
    };
    WidgetCardChart.prototype.tableResultComponent = function (_a) {
        var loading = _a.loading, errorMessage = _a.errorMessage, tableResults = _a.tableResults;
        var _b = this.props, location = _b.location, widget = _b.widget, organization = _b.organization;
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            // Align height to other charts.
            return <placeholder_1.default height="200px"/>;
        }
        return tableResults.map(function (result, i) {
            var _a, _b;
            var fields = (_b = (_a = widget.queries[i]) === null || _a === void 0 ? void 0 : _a.fields) !== null && _b !== void 0 ? _b : [];
            return (<StyledSimpleTableChart key={"table:" + result.title} location={location} fields={fields} title={tableResults.length > 1 ? result.title : ''} loading={loading} metadata={result.meta} data={result.data} organization={organization}/>);
        });
    };
    WidgetCardChart.prototype.bigNumberComponent = function (_a) {
        var loading = _a.loading, errorMessage = _a.errorMessage, tableResults = _a.tableResults;
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            return <BigNumber>{'\u2014'}</BigNumber>;
        }
        return tableResults.map(function (result) {
            var _a;
            var tableMeta = (_a = result.meta) !== null && _a !== void 0 ? _a : {};
            var fields = Object.keys(tableMeta !== null && tableMeta !== void 0 ? tableMeta : {});
            var field = fields[0];
            if (!field || !result.data.length) {
                return <BigNumber key={"big_number:" + result.title}>{'\u2014'}</BigNumber>;
            }
            var dataRow = result.data[0];
            var fieldRenderer = fieldRenderers_1.getFieldFormatter(field, tableMeta);
            var rendered = fieldRenderer(dataRow);
            return <BigNumber key={"big_number:" + result.title}>{rendered}</BigNumber>;
        });
    };
    WidgetCardChart.prototype.chartComponent = function (chartProps) {
        var widget = this.props.widget;
        switch (widget.displayType) {
            case 'bar':
                return <barChart_1.default {...chartProps}/>;
            case 'area':
                return <areaChart_1.default stacked {...chartProps}/>;
            case 'world_map':
                return <worldMapChart_1.default {...chartProps}/>;
            case 'line':
            default:
                return <lineChart_1.default {...chartProps}/>;
        }
    };
    WidgetCardChart.prototype.render = function () {
        var _this = this;
        var _a, _b, _c;
        var _d = this.props, theme = _d.theme, tableResults = _d.tableResults, timeseriesResults = _d.timeseriesResults, errorMessage = _d.errorMessage, loading = _d.loading, widget = _d.widget;
        if (widget.displayType === 'table') {
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.tableResultComponent({ tableResults: tableResults, loading: loading, errorMessage: errorMessage })}
        </transitionChart_1.default>);
        }
        if (widget.displayType === 'big_number') {
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.bigNumberComponent({ tableResults: tableResults, loading: loading, errorMessage: errorMessage })}
        </transitionChart_1.default>);
        }
        if (errorMessage) {
            return (<errorPanel_1.default>
          <icons_1.IconWarning color="gray500" size="lg"/>
        </errorPanel_1.default>);
        }
        var _e = this.props, location = _e.location, router = _e.router, selection = _e.selection;
        var _f = selection.datetime, start = _f.start, end = _f.end, period = _f.period, utc = _f.utc;
        if (widget.displayType === 'world_map') {
            var DEFAULT_GEO_DATA_1 = {
                title: '',
                data: [],
            };
            var processTableResults = function () {
                var _a;
                if (!tableResults || !tableResults.length) {
                    return DEFAULT_GEO_DATA_1;
                }
                var tableResult = tableResults[0];
                var data = tableResult.data, meta = tableResult.meta;
                if (!data || !data.length || !meta) {
                    return DEFAULT_GEO_DATA_1;
                }
                var preAggregate = Object.keys(meta).find(function (column) {
                    return column !== 'geo.country_code';
                });
                if (!preAggregate) {
                    return DEFAULT_GEO_DATA_1;
                }
                return {
                    title: (_a = tableResult.title) !== null && _a !== void 0 ? _a : '',
                    data: data
                        .filter(function (row) { return row['geo.country_code']; })
                        .map(function (row) {
                        return { name: row['geo.country_code'], value: row[preAggregate] };
                    }),
                };
            };
            var _g = processTableResults(), data = _g.data, title = _g.title;
            var series = [
                {
                    seriesName: title,
                    data: data,
                },
            ];
            return (<transitionChart_1.default loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          <ChartWrapper>
            {getDynamicText_1.default({
                    value: this.chartComponent({
                        series: series,
                    }),
                    fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                })}
          </ChartWrapper>
        </transitionChart_1.default>);
        }
        var legend = {
            left: 0,
            top: 0,
            selected: utils_1.getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = fields_1.getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = fields_1.getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
        };
        var axisField = (_c = (_b = (_a = widget.queries[0]) === null || _a === void 0 ? void 0 : _a.fields) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : 'count()';
        var chartOptions = {
            grid: {
                left: 0,
                right: 0,
                top: '40px',
                bottom: 0,
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: charts_1.tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return charts_1.axisLabelFormatter(value, axisField); },
                },
            },
        };
        return (<chartZoom_1.default router={router} period={period} start={start} end={end} utc={utc}>
        {function (zoomRenderProps) {
                if (errorMessage) {
                    return (<errorPanel_1.default>
                <icons_1.IconWarning color="gray500" size="lg"/>
              </errorPanel_1.default>);
                }
                var colors = timeseriesResults
                    ? theme.charts.getColorPalette(timeseriesResults.length - 2)
                    : [];
                // Create a list of series based on the order of the fields,
                var series = timeseriesResults
                    ? timeseriesResults.map(function (values, i) { return (tslib_1.__assign(tslib_1.__assign({}, values), { color: colors[i] })); })
                    : [];
                return (<transitionChart_1.default loading={loading} reloading={loading}>
              <LoadingScreen loading={loading}/>
              <ChartWrapper>
                {getDynamicText_1.default({
                        value: _this.chartComponent(tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, zoomRenderProps), chartOptions), { legend: legend, series: series })),
                        fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
                    })}
              </ChartWrapper>
            </transitionChart_1.default>);
            }}
      </chartZoom_1.default>);
    };
    return WidgetCardChart;
}(React.Component));
var StyledTransparentLoadingMask = styled_1.default(function (props) { return (<transparentLoadingMask_1.default {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
var LoadingScreen = function (_a) {
    var loading = _a.loading;
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <loadingIndicator_1.default mini/>
    </StyledTransparentLoadingMask>);
};
var BigNumber = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: 32px;\n  padding: ", " ", " ", " ", ";\n  * {\n    text-align: left !important;\n  }\n"], ["\n  font-size: 32px;\n  padding: ", " ", " ", " ", ";\n  * {\n    text-align: left !important;\n  }\n"])), space_1.default(1), space_1.default(3), space_1.default(3), space_1.default(3));
var ChartWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding: 0 ", " ", ";\n"], ["\n  padding: 0 ", " ", ";\n"])), space_1.default(3), space_1.default(3));
var StyledSimpleTableChart = styled_1.default(simpleTableChart_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n  font-size: ", ";\n  box-shadow: none;\n\n  > div {\n    padding: ", " ", ";\n  }\n"], ["\n  margin-top: ", ";\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n  font-size: ", ";\n  box-shadow: none;\n\n  > div {\n    padding: ", " ", ";\n  }\n"])), space_1.default(1.5), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(3));
exports.default = react_1.withTheme(WidgetCardChart);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=widgetCardChart.jsx.map