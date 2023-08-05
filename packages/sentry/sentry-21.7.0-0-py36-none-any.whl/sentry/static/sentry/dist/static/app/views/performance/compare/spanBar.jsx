Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var DividerHandlerManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/dividerHandlerManager"));
var utils_1 = require("app/components/events/interfaces/spans/utils");
var constants_1 = require("app/components/performance/waterfall/constants");
var row_1 = require("app/components/performance/waterfall/row");
var rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
var rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
var treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
var utils_2 = require("app/components/performance/waterfall/utils");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var spanDetail_1 = tslib_1.__importDefault(require("./spanDetail"));
var styles_1 = require("./styles");
var utils_3 = require("./utils");
var SpanBar = /** @class */ (function (_super) {
    tslib_1.__extends(SpanBar, _super);
    function SpanBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.renderDivider = function (dividerHandlerChildrenProps) {
            var theme = _this.props.theme;
            if (_this.state.showDetail) {
                // Mock component to preserve layout spacing
                return (<rowDivider_1.DividerLine style={{
                        position: 'relative',
                        backgroundColor: utils_2.getBackgroundColor({
                            theme: theme,
                            showDetail: true,
                        }),
                    }}/>);
            }
            var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
            return (<rowDivider_1.DividerLine ref={addDividerLineRef()} style={{
                    position: 'relative',
                }} onMouseEnter={function () {
                    dividerHandlerChildrenProps.setHover(true);
                }} onMouseLeave={function () {
                    dividerHandlerChildrenProps.setHover(false);
                }} onMouseOver={function () {
                    dividerHandlerChildrenProps.setHover(true);
                }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
                    // we prevent the propagation of the clicks from this component to prevent
                    // the span detail from being opened.
                    event.stopPropagation();
                }}/>);
        };
        _this.toggleDisplayDetail = function () {
            _this.setState(function (state) { return ({
                showDetail: !state.showDetail,
            }); });
        };
        return _this;
    }
    SpanBar.prototype.renderSpanTreeConnector = function (_a) {
        var hasToggler = _a.hasToggler;
        var _b = this.props, isLast = _b.isLast, isRoot = _b.isRoot, spanTreeDepth = _b.treeDepth, continuingTreeDepths = _b.continuingTreeDepths, span = _b.span, showSpanTree = _b.showSpanTree;
        var spanID = utils_3.getSpanID(span);
        if (isRoot) {
            if (hasToggler) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={spanID + "-last"} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingTreeDepths.map(function (treeDepth) {
            var depth = utils_1.unwrapTreeDepth(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            var left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left: left }} key={spanID + "-" + depth} orphanBranch={utils_1.isOrphanTreeDepth(treeDepth)}/>);
        });
        if (hasToggler && showSpanTree) {
            // if there is a toggle button, we add a connector bar to create an attachment
            // between the toggle button and any connector bars below the toggle button
            connectorBars.push(<treeConnector_1.ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? "-" + constants_1.ROW_HEIGHT / 2 + "px" : '0',
                    top: 'auto',
                }} key={spanID + "-last"} orphanBranch={false}/>);
        }
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={utils_3.isOrphanDiffSpan(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    };
    SpanBar.prototype.renderSpanTreeToggler = function (_a) {
        var _this = this;
        var left = _a.left;
        var _b = this.props, numOfSpanChildren = _b.numOfSpanChildren, isRoot = _b.isRoot, showSpanTree = _b.showSpanTree;
        var chevron = <treeConnector_1.StyledIconChevron direction={showSpanTree ? 'up' : 'down'}/>;
        if (numOfSpanChildren <= 0) {
            return (<treeConnector_1.TreeToggleContainer style={{ left: left + "px" }}>
          {this.renderSpanTreeConnector({ hasToggler: false })}
        </treeConnector_1.TreeToggleContainer>);
        }
        var chevronElement = !isRoot ? <div>{chevron}</div> : null;
        return (<treeConnector_1.TreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderSpanTreeConnector({ hasToggler: true })}
        <treeConnector_1.TreeToggle disabled={!!isRoot} isExpanded={this.props.showSpanTree} errored={false} onClick={function (event) {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                _this.props.toggleSpanTree();
            }}>
          <count_1.default value={numOfSpanChildren}/>
          {chevronElement}
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    };
    SpanBar.prototype.renderTitle = function () {
        var _a;
        var _b = this.props, span = _b.span, treeDepth = _b.treeDepth;
        var operationName = utils_3.getSpanOperation(span) ? (<strong>
        {utils_3.getSpanOperation(span)}
        {' \u2014 '}
      </strong>) : ('');
        var description = (_a = utils_3.getSpanDescription(span)) !== null && _a !== void 0 ? _a : (span.comparisonResult === 'matched' ? locale_1.t('matched') : utils_3.getSpanID(span));
        var left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2);
        return (<rowTitle_1.RowTitleContainer>
        {this.renderSpanTreeToggler({ left: left })}
        <rowTitle_1.RowTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          <span>
            {operationName}
            {description}
          </span>
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
    };
    SpanBar.prototype.getSpanBarStyles = function () {
        var _a = this.props, theme = _a.theme, span = _a.span, generateBounds = _a.generateBounds;
        var bounds = generateBounds(span);
        function normalizePadding(width) {
            if (!width) {
                return undefined;
            }
            return "max(1px, " + width + ")";
        }
        switch (span.comparisonResult) {
            case 'matched': {
                var baselineDuration = utils_3.getSpanDuration(span.baselineSpan);
                var regressionDuration = utils_3.getSpanDuration(span.regressionSpan);
                if (baselineDuration === regressionDuration) {
                    return {
                        background: {
                            color: undefined,
                            width: normalizePadding(utils_3.generateCSSWidth(bounds.background)),
                            hatch: true,
                        },
                        foreground: undefined,
                    };
                }
                if (baselineDuration > regressionDuration) {
                    return {
                        background: {
                            // baseline
                            color: theme.textColor,
                            width: normalizePadding(utils_3.generateCSSWidth(bounds.background)),
                        },
                        foreground: {
                            // regression
                            color: undefined,
                            width: normalizePadding(utils_3.generateCSSWidth(bounds.foreground)),
                            hatch: true,
                        },
                    };
                }
                // case: baselineDuration < regressionDuration
                return {
                    background: {
                        // regression
                        color: theme.purple200,
                        width: normalizePadding(utils_3.generateCSSWidth(bounds.background)),
                    },
                    foreground: {
                        // baseline
                        color: undefined,
                        width: normalizePadding(utils_3.generateCSSWidth(bounds.foreground)),
                        hatch: true,
                    },
                };
            }
            case 'regression': {
                return {
                    background: {
                        color: theme.purple200,
                        width: normalizePadding(utils_3.generateCSSWidth(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            case 'baseline': {
                return {
                    background: {
                        color: theme.textColor,
                        width: normalizePadding(utils_3.generateCSSWidth(bounds.background)),
                    },
                    foreground: undefined,
                };
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderComparisonReportLabel = function () {
        var span = this.props.span;
        switch (span.comparisonResult) {
            case 'matched': {
                var baselineDuration = utils_3.getSpanDuration(span.baselineSpan);
                var regressionDuration = utils_3.getSpanDuration(span.regressionSpan);
                var label = void 0;
                if (baselineDuration === regressionDuration) {
                    label = <ComparisonLabel>{locale_1.t('No change')}</ComparisonLabel>;
                }
                if (baselineDuration > regressionDuration) {
                    var duration = utils_2.getHumanDuration(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{locale_1.t('- %s faster', duration)}</NotableComparisonLabel>);
                }
                if (baselineDuration < regressionDuration) {
                    var duration = utils_2.getHumanDuration(Math.abs(baselineDuration - regressionDuration));
                    label = (<NotableComparisonLabel>{locale_1.t('+ %s slower', duration)}</NotableComparisonLabel>);
                }
                return label;
            }
            case 'baseline': {
                return <ComparisonLabel>{locale_1.t('Only in baseline')}</ComparisonLabel>;
            }
            case 'regression': {
                return <ComparisonLabel>{locale_1.t('Only in this event')}</ComparisonLabel>;
            }
            default: {
                var _exhaustiveCheck = span;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderHeader = function (dividerHandlerChildrenProps) {
        var _this = this;
        var _a, _b;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        var _c = this.props, spanNumber = _c.spanNumber, span = _c.span;
        var isMatched = span.comparisonResult === 'matched';
        var hideSpanBarColumn = this.state.showDetail && isMatched;
        var spanBarStyles = this.getSpanBarStyles();
        var foregroundSpanBar = spanBarStyles.foreground ? (<ComparisonSpanBarRectangle spanBarHatch={(_a = spanBarStyles.foreground.hatch) !== null && _a !== void 0 ? _a : false} style={{
                backgroundColor: spanBarStyles.foreground.color,
                width: spanBarStyles.foreground.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>) : null;
        return (<row_1.RowCellContainer showDetail={this.state.showDetail}>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
                width: "calc(" + utils_2.toPercent(dividerPosition) + " - 0.5px)",
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          {this.renderTitle()}
        </row_1.RowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
                width: "calc(" + utils_2.toPercent(1 - dividerPosition) + " - 0.5px)",
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          <SpanContainer>
            <ComparisonSpanBarRectangle spanBarHatch={(_b = spanBarStyles.background.hatch) !== null && _b !== void 0 ? _b : false} style={{
                backgroundColor: spanBarStyles.background.color,
                width: spanBarStyles.background.width,
                display: hideSpanBarColumn ? 'none' : 'block',
            }}/>
            {foregroundSpanBar}
          </SpanContainer>
          {this.renderComparisonReportLabel()}
        </row_1.RowCell>
        {!this.state.showDetail && (<rowDivider_1.DividerLineGhostContainer style={{
                    width: "calc(" + utils_2.toPercent(dividerPosition) + " + 0.5px)",
                    display: 'none',
                }}>
            <rowDivider_1.DividerLine ref={addGhostDividerLineRef()} style={{
                    right: 0,
                }} className="hovering" onClick={function (event) {
                    // the ghost divider line should not be interactive.
                    // we prevent the propagation of the clicks from this component to prevent
                    // the span detail from being opened.
                    event.stopPropagation();
                }}/>
          </rowDivider_1.DividerLineGhostContainer>)}
      </row_1.RowCellContainer>);
    };
    SpanBar.prototype.renderDetail = function () {
        if (!this.state.showDetail) {
            return null;
        }
        var _a = this.props, span = _a.span, generateBounds = _a.generateBounds;
        return <spanDetail_1.default span={this.props.span} bounds={generateBounds(span)}/>;
    };
    SpanBar.prototype.render = function () {
        var _this = this;
        return (<row_1.Row visible data-test-id="span-row">
        <DividerHandlerManager.Consumer>
          {function (dividerHandlerChildrenProps) { return _this.renderHeader(dividerHandlerChildrenProps); }}
        </DividerHandlerManager.Consumer>
        {this.renderDetail()}
      </row_1.Row>);
    };
    return SpanBar;
}(React.Component));
var ComparisonSpanBarRectangle = styled_1.default(styles_1.SpanBarRectangle)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  height: 16px;\n  ", "\n"], ["\n  position: absolute;\n  left: 0;\n  height: 16px;\n  ", "\n"])), function (p) { return utils_2.getHatchPattern(p, p.theme.purple200, p.theme.gray500); });
var ComparisonLabel = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  user-select: none;\n  right: ", ";\n  line-height: ", "px;\n  top: ", "px;\n  font-size: ", ";\n"], ["\n  position: absolute;\n  user-select: none;\n  right: ", ";\n  line-height: ", "px;\n  top: ", "px;\n  font-size: ", ";\n"])), space_1.default(1), constants_1.ROW_HEIGHT - 2 * constants_1.ROW_PADDING, constants_1.ROW_PADDING, function (p) { return p.theme.fontSizeExtraSmall; });
var SpanContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  margin-right: 120px;\n"], ["\n  position: relative;\n  margin-right: 120px;\n"])));
var NotableComparisonLabel = styled_1.default(ComparisonLabel)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
exports.default = react_1.withTheme(SpanBar);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=spanBar.jsx.map