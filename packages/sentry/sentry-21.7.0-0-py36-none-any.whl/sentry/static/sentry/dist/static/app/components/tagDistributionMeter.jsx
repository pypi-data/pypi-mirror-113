Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var TagDistributionMeter = /** @class */ (function (_super) {
    tslib_1.__extends(TagDistributionMeter, _super);
    function TagDistributionMeter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TagDistributionMeter.prototype.renderTitle = function () {
        var _a = this.props, segments = _a.segments, totalValues = _a.totalValues, title = _a.title, isLoading = _a.isLoading, hasError = _a.hasError, showReleasePackage = _a.showReleasePackage;
        if (!Array.isArray(segments) || segments.length <= 0) {
            return (<Title>
          <TitleType>{title}</TitleType>
        </Title>);
        }
        var largestSegment = segments[0];
        var pct = utils_1.percent(largestSegment.count, totalValues);
        var pctLabel = Math.floor(pct);
        var renderLabel = function () {
            switch (title) {
                case 'release':
                    return (<Label>
              <version_1.default version={largestSegment.name} anchor={false} tooltipRawVersion withPackage={showReleasePackage} truncate/>
            </Label>);
                default:
                    return <Label>{largestSegment.name || locale_1.t('n/a')}</Label>;
            }
        };
        return (<Title>
        <TitleType>{title}</TitleType>
        <TitleDescription>
          {renderLabel()}
          {isLoading || hasError ? null : <Percent>{pctLabel}%</Percent>}
        </TitleDescription>
      </Title>);
    };
    TagDistributionMeter.prototype.renderSegments = function () {
        var _a = this.props, segments = _a.segments, onTagClick = _a.onTagClick, title = _a.title, isLoading = _a.isLoading, hasError = _a.hasError, totalValues = _a.totalValues, renderLoading = _a.renderLoading, renderError = _a.renderError, renderEmpty = _a.renderEmpty, showReleasePackage = _a.showReleasePackage;
        if (isLoading) {
            return renderLoading();
        }
        if (hasError) {
            return <SegmentBar>{renderError()}</SegmentBar>;
        }
        if (totalValues === 0) {
            return <SegmentBar>{renderEmpty()}</SegmentBar>;
        }
        return (<SegmentBar>
        {segments.map(function (value, index) {
                var pct = utils_1.percent(value.count, totalValues);
                var pctLabel = Math.floor(pct);
                var renderTooltipValue = function () {
                    switch (title) {
                        case 'release':
                            return (<version_1.default version={value.name} anchor={false} withPackage={showReleasePackage}/>);
                        default:
                            return value.name || locale_1.t('n/a');
                    }
                };
                var tooltipHtml = (<React.Fragment>
              <div className="truncate">{renderTooltipValue()}</div>
              {pctLabel}%
            </React.Fragment>);
                var segmentProps = {
                    index: index,
                    to: value.url,
                    onClick: function () {
                        if (onTagClick) {
                            onTagClick(title, value);
                        }
                    },
                };
                return (<div key={value.value} style={{ width: pct + '%' }}>
              <tooltip_1.default title={tooltipHtml} containerDisplayMode="block">
                {value.isOther ? <OtherSegment /> : <Segment {...segmentProps}/>}
              </tooltip_1.default>
            </div>);
            })}
      </SegmentBar>);
    };
    TagDistributionMeter.prototype.render = function () {
        var _a = this.props, segments = _a.segments, totalValues = _a.totalValues;
        var totalVisible = segments.reduce(function (sum, value) { return sum + value.count; }, 0);
        var hasOther = totalVisible < totalValues;
        if (hasOther) {
            segments.push({
                isOther: true,
                name: locale_1.t('Other'),
                value: 'other',
                count: totalValues - totalVisible,
                url: '',
            });
        }
        return (<TagSummary>
        {this.renderTitle()}
        {this.renderSegments()}
      </TagSummary>);
    };
    TagDistributionMeter.defaultProps = {
        isLoading: false,
        hasError: false,
        renderLoading: function () { return null; },
        renderEmpty: function () { return <p>{locale_1.t('No recent data.')}</p>; },
        renderError: function () { return null; },
        showReleasePackage: false,
    };
    return TagDistributionMeter;
}(React.Component));
exports.default = TagDistributionMeter;
var COLORS = [
    '#3A3387',
    '#5F40A3',
    '#8C4FBD',
    '#B961D3',
    '#DE76E4',
    '#EF91E8',
    '#F7B2EC',
    '#FCD8F4',
    '#FEEBF9',
];
var TagSummary = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var SegmentBar = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  overflow: hidden;\n  border-radius: 2px;\n"], ["\n  display: flex;\n  overflow: hidden;\n  border-radius: 2px;\n"])));
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  font-size: ", ";\n  justify-content: space-between;\n"], ["\n  display: flex;\n  font-size: ", ";\n  justify-content: space-between;\n"])), function (p) { return p.theme.fontSizeSmall; });
var TitleType = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: bold;\n  ", ";\n"], ["\n  color: ", ";\n  font-weight: bold;\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var TitleDescription = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  color: ", ";\n  text-align: right;\n"], ["\n  display: flex;\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.gray300; });
var Label = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n  max-width: 150px;\n"], ["\n  ", ";\n  max-width: 150px;\n"])), overflowEllipsis_1.default);
var Percent = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  padding-left: ", ";\n  color: ", ";\n"], ["\n  font-weight: bold;\n  padding-left: ", ";\n  color: ", ";\n"])), space_1.default(0.5), function (p) { return p.theme.textColor; });
var OtherSegment = styled_1.default('span')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"], ["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"])), COLORS[COLORS.length - 1]);
var Segment = styled_1.default(react_router_1.Link, { shouldForwardProp: is_prop_valid_1.default })(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"], ["\n  display: block;\n  width: 100%;\n  height: 16px;\n  color: inherit;\n  outline: none;\n  background-color: ", ";\n"])), function (p) { return COLORS[p.index]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=tagDistributionMeter.jsx.map