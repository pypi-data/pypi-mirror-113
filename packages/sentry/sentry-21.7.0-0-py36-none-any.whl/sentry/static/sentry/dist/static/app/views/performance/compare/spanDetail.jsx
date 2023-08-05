Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var spanDetail_1 = require("app/components/events/interfaces/spans/spanDetail");
var types_1 = require("app/components/events/interfaces/spans/types");
var utils_1 = require("app/components/performance/waterfall/utils");
var pill_1 = tslib_1.__importDefault(require("app/components/pill"));
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var spanDetailContent_1 = tslib_1.__importDefault(require("./spanDetailContent"));
var styles_1 = require("./styles");
var utils_2 = require("./utils");
var getDurationDisplay = function (width) {
    if (!width) {
        return 'right';
    }
    switch (width.type) {
        case 'WIDTH_PIXEL': {
            return 'right';
        }
        case 'WIDTH_PERCENTAGE': {
            var spaceNeeded = 0.3;
            if (width.width < 1 - spaceNeeded) {
                return 'right';
            }
            return 'inset';
        }
        default: {
            var _exhaustiveCheck = width;
            return _exhaustiveCheck;
        }
    }
};
var SpanDetail = /** @class */ (function (_super) {
    tslib_1.__extends(SpanDetail, _super);
    function SpanDetail() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SpanDetail.prototype.renderContent = function () {
        var _a = this.props, span = _a.span, bounds = _a.bounds;
        switch (span.comparisonResult) {
            case 'matched': {
                return (<MatchedSpanDetailsContent baselineSpan={span.baselineSpan} regressionSpan={span.regressionSpan} bounds={bounds}/>);
            }
            case 'regression': {
                return <spanDetailContent_1.default span={span.regressionSpan}/>;
            }
            case 'baseline': {
                return <spanDetailContent_1.default span={span.baselineSpan}/>;
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanDetail.prototype.render = function () {
        return (<spanDetail_1.SpanDetailContainer onClick={function (event) {
                // prevent toggling the span detail
                event.stopPropagation();
            }}>
        {this.renderContent()}
      </spanDetail_1.SpanDetailContainer>);
    };
    return SpanDetail;
}(React.Component));
var MatchedSpanDetailsContent = function (props) {
    var _a, _b;
    var baselineSpan = props.baselineSpan, regressionSpan = props.regressionSpan, bounds = props.bounds;
    var dataKeys = new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.keys((_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {}))), tslib_1.__read(Object.keys((_b = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _b !== void 0 ? _b : {}))));
    var unknownKeys = new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(Object.keys(baselineSpan).filter(function (key) {
        return !types_1.rawSpanKeys.has(key);
    }))), tslib_1.__read(Object.keys(regressionSpan).filter(function (key) {
        return !types_1.rawSpanKeys.has(key);
    }))));
    return (<div>
      <SpanBars bounds={bounds} baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      <Row baselineTitle={locale_1.t('Baseline Span ID')} regressionTitle={locale_1.t("This Event's Span ID")} renderBaselineContent={function () { return baselineSpan.span_id; }} renderRegressionContent={function () { return regressionSpan.span_id; }}/>
      <Row title={locale_1.t('Parent Span ID')} renderBaselineContent={function () { return baselineSpan.parent_span_id || ''; }} renderRegressionContent={function () { return regressionSpan.parent_span_id || ''; }}/>
      <Row title={locale_1.t('Trace ID')} renderBaselineContent={function () { return baselineSpan.trace_id; }} renderRegressionContent={function () { return regressionSpan.trace_id; }}/>
      <Row title={locale_1.t('Description')} renderBaselineContent={function () { var _a; return (_a = baselineSpan.description) !== null && _a !== void 0 ? _a : ''; }} renderRegressionContent={function () { var _a; return (_a = regressionSpan.description) !== null && _a !== void 0 ? _a : ''; }}/>
      <Row title={locale_1.t('Start Date')} renderBaselineContent={function () {
            return getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                <dateTime_1.default date={baselineSpan.start_timestamp * 1000}/>
                {" (" + baselineSpan.start_timestamp + ")"}
              </React.Fragment>),
            });
        }} renderRegressionContent={function () {
            return getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                <dateTime_1.default date={regressionSpan.start_timestamp * 1000}/>
                {" (" + baselineSpan.start_timestamp + ")"}
              </React.Fragment>),
            });
        }}/>
      <Row title={locale_1.t('End Date')} renderBaselineContent={function () {
            return getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                <dateTime_1.default date={baselineSpan.timestamp * 1000}/>
                {" (" + baselineSpan.timestamp + ")"}
              </React.Fragment>),
            });
        }} renderRegressionContent={function () {
            return getDynamicText_1.default({
                fixed: 'Mar 16, 2020 9:10:12 AM UTC',
                value: (<React.Fragment>
                <dateTime_1.default date={regressionSpan.timestamp * 1000}/>
                {" (" + regressionSpan.timestamp + ")"}
              </React.Fragment>),
            });
        }}/>
      <Row title={locale_1.t('Duration')} renderBaselineContent={function () {
            var startTimestamp = baselineSpan.start_timestamp;
            var endTimestamp = baselineSpan.timestamp;
            var duration = (endTimestamp - startTimestamp) * 1000;
            return duration.toFixed(3) + "ms";
        }} renderRegressionContent={function () {
            var startTimestamp = regressionSpan.start_timestamp;
            var endTimestamp = regressionSpan.timestamp;
            var duration = (endTimestamp - startTimestamp) * 1000;
            return duration.toFixed(3) + "ms";
        }}/>
      <Row title={locale_1.t('Operation')} renderBaselineContent={function () { return baselineSpan.op || ''; }} renderRegressionContent={function () { return regressionSpan.op || ''; }}/>
      <Row title={locale_1.t('Same Process as Parent')} renderBaselineContent={function () { return String(!!baselineSpan.same_process_as_parent); }} renderRegressionContent={function () { return String(!!regressionSpan.same_process_as_parent); }}/>
      <Tags baselineSpan={baselineSpan} regressionSpan={regressionSpan}/>
      {Array.from(dataKeys).map(function (dataTitle) { return (<Row key={dataTitle} title={dataTitle} renderBaselineContent={function () {
                var _a;
                var data = (_a = baselineSpan === null || baselineSpan === void 0 ? void 0 : baselineSpan.data) !== null && _a !== void 0 ? _a : {};
                var value = data[dataTitle];
                return JSON.stringify(value, null, 4) || '';
            }} renderRegressionContent={function () {
                var _a;
                var data = (_a = regressionSpan === null || regressionSpan === void 0 ? void 0 : regressionSpan.data) !== null && _a !== void 0 ? _a : {};
                var value = data[dataTitle];
                return JSON.stringify(value, null, 4) || '';
            }}/>); })}
      {Array.from(unknownKeys).map(function (key) { return (<Row key={key} title={key} renderBaselineContent={function () {
                return JSON.stringify(baselineSpan[key], null, 4) || '';
            }} renderRegressionContent={function () {
                return JSON.stringify(regressionSpan[key], null, 4) || '';
            }}/>); })}
    </div>);
};
var RowSplitter = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n\n  > * + * {\n    border-left: 1px solid ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n\n  > * + * {\n    border-left: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.border; });
var SpanBarContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  height: 16px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  position: relative;\n  height: 16px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(3), space_1.default(2));
var SpanBars = function (props) {
    var bounds = props.bounds, baselineSpan = props.baselineSpan, regressionSpan = props.regressionSpan;
    var baselineDurationDisplay = getDurationDisplay(bounds.baseline);
    var regressionDurationDisplay = getDurationDisplay(bounds.regression);
    return (<RowSplitter>
      <RowContainer>
        <SpanBarContainer>
          <styles_1.SpanBarRectangle style={{
            backgroundColor: theme_1.default.gray500,
            width: utils_2.generateCSSWidth(bounds.baseline),
            position: 'absolute',
            height: '16px',
        }}>
            <DurationPill durationDisplay={baselineDurationDisplay} fontColors={{ right: theme_1.default.gray500, inset: theme_1.default.white }}>
              {utils_1.getHumanDuration(utils_2.getSpanDuration(baselineSpan))}
            </DurationPill>
          </styles_1.SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
      <RowContainer>
        <SpanBarContainer>
          <styles_1.SpanBarRectangle style={{
            backgroundColor: theme_1.default.purple200,
            width: utils_2.generateCSSWidth(bounds.regression),
            position: 'absolute',
            height: '16px',
        }}>
            <DurationPill durationDisplay={regressionDurationDisplay} fontColors={{ right: theme_1.default.gray500, inset: theme_1.default.gray500 }}>
              {utils_1.getHumanDuration(utils_2.getSpanDuration(regressionSpan))}
            </DurationPill>
          </styles_1.SpanBarRectangle>
        </SpanBarContainer>
      </RowContainer>
    </RowSplitter>);
};
var Row = function (props) {
    var _a, _b;
    var title = props.title, baselineTitle = props.baselineTitle, regressionTitle = props.regressionTitle;
    var baselineContent = props.renderBaselineContent();
    var regressionContent = props.renderRegressionContent();
    if (!baselineContent && !regressionContent) {
        return null;
    }
    return (<RowSplitter>
      <RowCell title={(_a = baselineTitle !== null && baselineTitle !== void 0 ? baselineTitle : title) !== null && _a !== void 0 ? _a : ''}>{baselineContent}</RowCell>
      <RowCell title={(_b = regressionTitle !== null && regressionTitle !== void 0 ? regressionTitle : title) !== null && _b !== void 0 ? _b : ''}>{regressionContent}</RowCell>
    </RowSplitter>);
};
var RowContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 50%;\n  min-width: 50%;\n  max-width: 50%;\n  flex-basis: 50%;\n\n  padding-left: ", ";\n  padding-right: ", ";\n"], ["\n  width: 50%;\n  min-width: 50%;\n  max-width: 50%;\n  flex-basis: 50%;\n\n  padding-left: ", ";\n  padding-right: ", ";\n"])), space_1.default(2), space_1.default(2));
var RowTitle = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 13px;\n  font-weight: 600;\n"], ["\n  font-size: 13px;\n  font-weight: 600;\n"])));
var RowCell = function (_a) {
    var title = _a.title, children = _a.children;
    return (<RowContainer>
      <RowTitle>{title}</RowTitle>
      <div>
        <pre className="val" style={{ marginBottom: space_1.default(1) }}>
          <span className="val-string">{children}</span>
        </pre>
      </div>
    </RowContainer>);
};
var getTags = function (span) {
    var tags = span === null || span === void 0 ? void 0 : span.tags;
    if (!tags) {
        return undefined;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return undefined;
    }
    return tags;
};
var TagPills = function (_a) {
    var tags = _a.tags;
    if (!tags) {
        return null;
    }
    var keys = Object.keys(tags);
    if (keys.length <= 0) {
        return null;
    }
    return (<pills_1.default>
      {keys.map(function (key, index) { return (<pill_1.default key={index} name={key} value={String(tags[key]) || ''}/>); })}
    </pills_1.default>);
};
var Tags = function (_a) {
    var baselineSpan = _a.baselineSpan, regressionSpan = _a.regressionSpan;
    var baselineTags = getTags(baselineSpan);
    var regressionTags = getTags(regressionSpan);
    if (!baselineTags && !regressionTags) {
        return null;
    }
    return (<RowSplitter>
      <RowContainer>
        <RowTitle>{locale_1.t('Tags')}</RowTitle>
        <div>
          <TagPills tags={baselineTags}/>
        </div>
      </RowContainer>
      <RowContainer>
        <RowTitle>{locale_1.t('Tags')}</RowTitle>
        <div>
          <TagPills tags={regressionTags}/>
        </div>
      </RowContainer>
    </RowSplitter>);
};
var DurationPill = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ", ";\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"], ["\n  position: absolute;\n  top: 50%;\n  display: flex;\n  align-items: center;\n  transform: translateY(-50%);\n  white-space: nowrap;\n  font-size: ", ";\n  color: ", ";\n\n  ", ";\n\n  @media (max-width: ", ") {\n    font-size: 10px;\n  }\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.fontColors.right; }, function (p) {
    switch (p.durationDisplay) {
        case 'right':
            return "left: calc(100% + " + space_1.default(0.75) + ");";
        default:
            return "\n          right: " + space_1.default(0.75) + ";\n          color: " + p.fontColors.inset + ";\n        ";
    }
}, function (p) { return p.theme.breakpoints[1]; });
exports.default = SpanDetail;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=spanDetail.jsx.map