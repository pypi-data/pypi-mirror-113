Object.defineProperty(exports, "__esModule", { value: true });
exports.SecondaryHeader = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var opsBreakdown_1 = tslib_1.__importDefault(require("app/components/events/opsBreakdown"));
var miniHeader_1 = require("app/components/performance/waterfall/miniHeader");
var utils_1 = require("app/components/performance/waterfall/utils");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var constants_1 = require("./constants");
var CursorGuideHandler = tslib_1.__importStar(require("./cursorGuideHandler"));
var DividerHandlerManager = tslib_1.__importStar(require("./dividerHandlerManager"));
var measurementsPanel_1 = tslib_1.__importDefault(require("./measurementsPanel"));
var ScrollbarManager = tslib_1.__importStar(require("./scrollbarManager"));
var types_1 = require("./types");
var utils_2 = require("./utils");
var TraceViewHeader = /** @class */ (function (_super) {
    tslib_1.__extends(TraceViewHeader, _super);
    function TraceViewHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            minimapWidth: undefined,
        };
        return _this;
    }
    TraceViewHeader.prototype.componentDidMount = function () {
        this.fetchMinimapWidth();
    };
    TraceViewHeader.prototype.componentDidUpdate = function () {
        this.fetchMinimapWidth();
    };
    TraceViewHeader.prototype.fetchMinimapWidth = function () {
        var minimapInteractiveRef = this.props.minimapInteractiveRef;
        if (minimapInteractiveRef.current) {
            var minimapWidth = minimapInteractiveRef.current.getBoundingClientRect().width;
            if (minimapWidth !== this.state.minimapWidth) {
                // eslint-disable-next-line react/no-did-update-set-state
                this.setState({
                    minimapWidth: minimapWidth,
                });
            }
        }
    };
    TraceViewHeader.prototype.renderCursorGuide = function (_a) {
        var cursorGuideHeight = _a.cursorGuideHeight, showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        return (<CursorGuide style={{
                left: utils_1.toPercent(mouseLeft),
                height: cursorGuideHeight + "px",
            }}/>);
    };
    TraceViewHeader.prototype.renderViewHandles = function (_a) {
        var isDragging = _a.isDragging, onLeftHandleDragStart = _a.onLeftHandleDragStart, leftHandlePosition = _a.leftHandlePosition, onRightHandleDragStart = _a.onRightHandleDragStart, rightHandlePosition = _a.rightHandlePosition, viewWindowStart = _a.viewWindowStart, viewWindowEnd = _a.viewWindowEnd;
        var leftHandleGhost = isDragging ? (<Handle left={viewWindowStart} onMouseDown={function () {
                // do nothing
            }} isDragging={false}/>) : null;
        var leftHandle = (<Handle left={leftHandlePosition} onMouseDown={onLeftHandleDragStart} isDragging={isDragging}/>);
        var rightHandle = (<Handle left={rightHandlePosition} onMouseDown={onRightHandleDragStart} isDragging={isDragging}/>);
        var rightHandleGhost = isDragging ? (<Handle left={viewWindowEnd} onMouseDown={function () {
                // do nothing
            }} isDragging={false}/>) : null;
        return (<React.Fragment>
        {leftHandleGhost}
        {rightHandleGhost}
        {leftHandle}
        {rightHandle}
      </React.Fragment>);
    };
    TraceViewHeader.prototype.renderFog = function (dragProps) {
        return (<React.Fragment>
        <Fog style={{ height: '100%', width: utils_1.toPercent(dragProps.viewWindowStart) }}/>
        <Fog style={{
                height: '100%',
                width: utils_1.toPercent(1 - dragProps.viewWindowEnd),
                left: utils_1.toPercent(dragProps.viewWindowEnd),
            }}/>
      </React.Fragment>);
    };
    TraceViewHeader.prototype.renderDurationGuide = function (_a) {
        var showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        if (!showCursorGuide || !mouseLeft) {
            return null;
        }
        var interactiveLayer = this.props.minimapInteractiveRef.current;
        if (!interactiveLayer) {
            return null;
        }
        var rect = utils_1.rectOfContent(interactiveLayer);
        var trace = this.props.trace;
        var duration = mouseLeft * Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        var style = { top: 0, left: "calc(" + mouseLeft * 100 + "% + 4px)" };
        var alignLeft = (1 - mouseLeft) * rect.width <= 100;
        return (<DurationGuideBox style={style} alignLeft={alignLeft}>
        <span>{utils_1.getHumanDuration(duration)}</span>
      </DurationGuideBox>);
    };
    TraceViewHeader.prototype.renderTicks = function () {
        var trace = this.props.trace;
        var minimapWidth = this.state.minimapWidth;
        var duration = Math.abs(trace.traceEndTimestamp - trace.traceStartTimestamp);
        var numberOfParts = 5;
        if (minimapWidth) {
            if (minimapWidth <= 350) {
                numberOfParts = 4;
            }
            if (minimapWidth <= 280) {
                numberOfParts = 3;
            }
            if (minimapWidth <= 160) {
                numberOfParts = 2;
            }
            if (minimapWidth <= 130) {
                numberOfParts = 1;
            }
        }
        if (numberOfParts === 1) {
            return (<TickLabel key="1" duration={duration * 0.5} style={{
                    left: utils_1.toPercent(0.5),
                }}/>);
        }
        var segment = 1 / (numberOfParts - 1);
        var ticks = [];
        for (var currentPart = 0; currentPart < numberOfParts; currentPart++) {
            if (currentPart === 0) {
                ticks.push(<TickLabel key="first" align={types_1.TickAlignment.Left} hideTickMarker duration={0} style={{
                        left: space_1.default(1),
                    }}/>);
                continue;
            }
            if (currentPart === numberOfParts - 1) {
                ticks.push(<TickLabel key="last" duration={duration} align={types_1.TickAlignment.Right} hideTickMarker style={{
                        right: space_1.default(1),
                    }}/>);
                continue;
            }
            var progress = segment * currentPart;
            ticks.push(<TickLabel key={String(currentPart)} duration={duration * progress} style={{
                    left: utils_1.toPercent(progress),
                }}/>);
        }
        return ticks;
    };
    TraceViewHeader.prototype.renderTimeAxis = function (_a) {
        var showCursorGuide = _a.showCursorGuide, mouseLeft = _a.mouseLeft;
        return (<TimeAxis>
        {this.renderTicks()}
        {this.renderCursorGuide({
                showCursorGuide: showCursorGuide,
                mouseLeft: mouseLeft,
                cursorGuideHeight: constants_1.TIME_AXIS_HEIGHT,
            })}
        {this.renderDurationGuide({
                showCursorGuide: showCursorGuide,
                mouseLeft: mouseLeft,
            })}
      </TimeAxis>);
    };
    TraceViewHeader.prototype.renderWindowSelection = function (dragProps) {
        if (!dragProps.isWindowSelectionDragging) {
            return null;
        }
        var left = Math.min(dragProps.windowSelectionInitial, dragProps.windowSelectionCurrent);
        return (<WindowSelection style={{
                left: utils_1.toPercent(left),
                width: utils_1.toPercent(dragProps.windowSelectionSize),
            }}/>);
    };
    TraceViewHeader.prototype.generateBounds = function () {
        var _a = this.props, dragProps = _a.dragProps, trace = _a.trace;
        return utils_2.boundsGenerator({
            traceStartTimestamp: trace.traceStartTimestamp,
            traceEndTimestamp: trace.traceEndTimestamp,
            viewStart: dragProps.viewWindowStart,
            viewEnd: dragProps.viewWindowEnd,
        });
    };
    TraceViewHeader.prototype.renderSecondaryHeader = function () {
        var _this = this;
        var _a;
        var event = this.props.event;
        var hasMeasurements = Object.keys((_a = event.measurements) !== null && _a !== void 0 ? _a : {}).length > 0;
        return (<DividerHandlerManager.Consumer>
        {function (dividerHandlerChildrenProps) {
                var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
                return (<exports.SecondaryHeader>
              <ScrollbarManager.Consumer>
                {function (_a) {
                        var virtualScrollbarRef = _a.virtualScrollbarRef, scrollBarAreaRef = _a.scrollBarAreaRef, onDragStart = _a.onDragStart, onScroll = _a.onScroll;
                        return (<miniHeader_1.ScrollbarContainer ref={_this.props.virtualScrollBarContainerRef} style={{
                                // the width of this component is shrunk to compensate for half of the width of the divider line
                                width: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                            }} onScroll={onScroll}>
                      <div style={{
                                width: 0,
                                height: '1px',
                            }} ref={scrollBarAreaRef}/>
                      <miniHeader_1.VirtualScrollbar data-type="virtual-scrollbar" ref={virtualScrollbarRef} onMouseDown={onDragStart}>
                        <miniHeader_1.VirtualScrollbarGrip />
                      </miniHeader_1.VirtualScrollbar>
                    </miniHeader_1.ScrollbarContainer>);
                    }}
              </ScrollbarManager.Consumer>
              <miniHeader_1.DividerSpacer />
              {hasMeasurements ? (<measurementsPanel_1.default event={event} generateBounds={_this.generateBounds()} dividerPosition={dividerPosition}/>) : null}
            </exports.SecondaryHeader>);
            }}
      </DividerHandlerManager.Consumer>);
    };
    TraceViewHeader.prototype.render = function () {
        var _this = this;
        return (<HeaderContainer>
        <DividerHandlerManager.Consumer>
          {function (dividerHandlerChildrenProps) {
                var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
                return (<React.Fragment>
                <OperationsBreakdown style={{
                        width: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                    }}>
                  {_this.props.event && (<opsBreakdown_1.default operationNameFilters={_this.props.operationNameFilters} event={_this.props.event} topN={3} hideHeader/>)}
                </OperationsBreakdown>
                <miniHeader_1.DividerSpacer style={{
                        position: 'absolute',
                        top: 0,
                        left: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                        height: constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT + "px",
                    }}/>
                <ActualMinimap trace={_this.props.trace} dividerPosition={dividerPosition}/>
                <CursorGuideHandler.Consumer>
                  {function (_a) {
                        var displayCursorGuide = _a.displayCursorGuide, hideCursorGuide = _a.hideCursorGuide, mouseLeft = _a.mouseLeft, showCursorGuide = _a.showCursorGuide;
                        return (<RightSidePane ref={_this.props.minimapInteractiveRef} style={{
                                width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
                                left: "calc(" + utils_1.toPercent(dividerPosition) + " + 0.5px)",
                            }} onMouseEnter={function (event) {
                                displayCursorGuide(event.pageX);
                            }} onMouseLeave={function () {
                                hideCursorGuide();
                            }} onMouseMove={function (event) {
                                displayCursorGuide(event.pageX);
                            }} onMouseDown={function (event) {
                                var target = event.target;
                                if (target instanceof Element &&
                                    target.getAttribute &&
                                    target.getAttribute('data-ignore')) {
                                    // ignore this event if we need to
                                    return;
                                }
                                _this.props.dragProps.onWindowSelectionDragStart(event);
                            }}>
                      <MinimapContainer>
                        {_this.renderFog(_this.props.dragProps)}
                        {_this.renderCursorGuide({
                                showCursorGuide: showCursorGuide,
                                mouseLeft: mouseLeft,
                                cursorGuideHeight: constants_1.MINIMAP_HEIGHT,
                            })}
                        {_this.renderViewHandles(_this.props.dragProps)}
                        {_this.renderWindowSelection(_this.props.dragProps)}
                      </MinimapContainer>
                      {_this.renderTimeAxis({
                                showCursorGuide: showCursorGuide,
                                mouseLeft: mouseLeft,
                            })}
                    </RightSidePane>);
                    }}
                </CursorGuideHandler.Consumer>
                {_this.renderSecondaryHeader()}
              </React.Fragment>);
            }}
        </DividerHandlerManager.Consumer>
      </HeaderContainer>);
    };
    return TraceViewHeader;
}(React.Component));
var ActualMinimap = /** @class */ (function (_super) {
    tslib_1.__extends(ActualMinimap, _super);
    function ActualMinimap() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ActualMinimap.prototype.renderRootSpan = function () {
        var trace = this.props.trace;
        var generateBounds = utils_2.boundsGenerator({
            traceStartTimestamp: trace.traceStartTimestamp,
            traceEndTimestamp: trace.traceEndTimestamp,
            viewStart: 0,
            viewEnd: 1,
        });
        var rootSpan = {
            trace_id: trace.traceID,
            span_id: trace.rootSpanID,
            start_timestamp: trace.traceStartTimestamp,
            timestamp: trace.traceEndTimestamp,
            op: trace.op,
            data: {},
        };
        return this.renderSpan({
            spanNumber: 0,
            generateBounds: generateBounds,
            span: rootSpan,
            childSpans: trace.childSpans,
        }).spanTree;
    };
    ActualMinimap.prototype.getBounds = function (bounds) {
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL':
            case 'INVALID_VIEW_WINDOW': {
                return {
                    left: utils_1.toPercent(0),
                    width: '0px',
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                return {
                    left: utils_1.toPercent(bounds.start),
                    width: bounds.width + "px",
                };
            }
            case 'TIMESTAMPS_REVERSED':
            case 'TIMESTAMPS_STABLE': {
                return {
                    left: utils_1.toPercent(bounds.start),
                    width: utils_1.toPercent(bounds.end - bounds.start),
                };
            }
            default: {
                var _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    };
    ActualMinimap.prototype.renderSpan = function (_a) {
        var _this = this;
        var _b;
        var spanNumber = _a.spanNumber, childSpans = _a.childSpans, generateBounds = _a.generateBounds, span = _a.span;
        var spanBarColour = utils_1.pickBarColour(utils_2.getSpanOperation(span));
        var bounds = generateBounds({
            startTimestamp: span.start_timestamp,
            endTimestamp: span.timestamp,
        });
        var _c = this.getBounds(bounds), spanLeft = _c.left, spanWidth = _c.width;
        var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[utils_2.getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = tslib_1.__assign({}, childSpans);
        delete childSpans[utils_2.getSpanID(span)];
        var reduced = spanChildren.reduce(function (acc, spanChild, index) {
            var key = "" + utils_2.getSpanID(spanChild, String(index));
            var results = _this.renderSpan({
                spanNumber: acc.nextSpanNumber,
                childSpans: childSpans,
                generateBounds: generateBounds,
                span: spanChild,
            });
            acc.renderedSpanChildren.push(<React.Fragment key={key}>{results.spanTree}</React.Fragment>);
            acc.nextSpanNumber = results.nextSpanNumber;
            return acc;
        }, {
            renderedSpanChildren: [],
            nextSpanNumber: spanNumber + 1,
        });
        return {
            nextSpanNumber: reduced.nextSpanNumber,
            spanTree: (<React.Fragment>
          <MinimapSpanBar style={{
                    backgroundColor: spanBarColour,
                    left: spanLeft,
                    width: spanWidth,
                }}/>
          {reduced.renderedSpanChildren}
        </React.Fragment>),
        };
    };
    ActualMinimap.prototype.render = function () {
        var dividerPosition = this.props.dividerPosition;
        return (<MinimapBackground style={{
                // the width of this component is shrunk to compensate for half of the width of the divider line
                width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
                left: "calc(" + utils_1.toPercent(dividerPosition) + " + 0.5px)",
            }}>
        <BackgroundSlider id="minimap-background-slider">
          {this.renderRootSpan()}
        </BackgroundSlider>
      </MinimapBackground>);
    };
    return ActualMinimap;
}(React.PureComponent));
var TimeAxis = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  position: absolute;\n  left: 0;\n  top: ", "px;\n  border-top: 1px solid ", ";\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  font-size: 10px;\n  font-weight: 500;\n  overflow: hidden;\n"], ["\n  width: 100%;\n  position: absolute;\n  left: 0;\n  top: ", "px;\n  border-top: 1px solid ", ";\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  font-size: 10px;\n  font-weight: 500;\n  overflow: hidden;\n"])), constants_1.MINIMAP_HEIGHT, function (p) { return p.theme.border; }, constants_1.TIME_AXIS_HEIGHT, function (p) { return p.theme.background; }, function (p) { return p.theme.gray300; });
var TickLabelContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n  display: flex;\n  align-items: center;\n  user-select: none;\n"], ["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n  display: flex;\n  align-items: center;\n  user-select: none;\n"])), constants_1.TIME_AXIS_HEIGHT);
var TickText = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"], ["\n  position: absolute;\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"])), function (_a) {
    var align = _a.align;
    switch (align) {
        case types_1.TickAlignment.Center: {
            return 'transform: translateX(-50%)';
        }
        case types_1.TickAlignment.Left: {
            return null;
        }
        case types_1.TickAlignment.Right: {
            return 'transform: translateX(-100%)';
        }
        default: {
            throw Error("Invalid tick alignment: " + align);
        }
    }
});
var TickMarker = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 1px;\n  height: 4px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  transform: translateX(-50%);\n"], ["\n  width: 1px;\n  height: 4px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  transform: translateX(-50%);\n"])), function (p) { return p.theme.gray200; });
var TickLabel = function (props) {
    var style = props.style, duration = props.duration, _a = props.hideTickMarker, hideTickMarker = _a === void 0 ? false : _a, _b = props.align, align = _b === void 0 ? types_1.TickAlignment.Center : _b;
    return (<TickLabelContainer style={style}>
      {hideTickMarker ? null : <TickMarker />}
      <TickText align={align}>{utils_1.getHumanDuration(duration)}</TickText>
    </TickLabelContainer>);
};
var DurationGuideBox = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  background-color: ", ";\n  padding: 4px;\n  height: 100%;\n  border-radius: 3px;\n  border: 1px solid rgba(0, 0, 0, 0.1);\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"], ["\n  position: absolute;\n  background-color: ", ";\n  padding: 4px;\n  height: 100%;\n  border-radius: 3px;\n  border: 1px solid rgba(0, 0, 0, 0.1);\n  line-height: 1;\n  white-space: nowrap;\n\n  ", ";\n"])), function (p) { return p.theme.background; }, function (_a) {
    var alignLeft = _a.alignLeft;
    if (!alignLeft) {
        return null;
    }
    return 'transform: translateX(-100%) translateX(-8px);';
});
var HeaderContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  position: sticky;\n  left: 0;\n  top: ", ";\n  z-index: ", ";\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  height: ", "px;\n  border-top-left-radius: ", ";\n  border-top-right-radius: ", ";\n"], ["\n  width: 100%;\n  position: sticky;\n  left: 0;\n  top: ", ";\n  z-index: ", ";\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n  height: ", "px;\n  border-top-left-radius: ", ";\n  border-top-right-radius: ", ";\n"])), function (p) { return (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0); }, function (p) { return p.theme.zIndex.traceView.minimapContainer; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, constants_1.MINIMAP_CONTAINER_HEIGHT, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var MinimapBackground = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  max-height: ", "px;\n  overflow: hidden;\n  position: absolute;\n  top: 0;\n"], ["\n  height: ", "px;\n  max-height: ", "px;\n  overflow: hidden;\n  position: absolute;\n  top: 0;\n"])), constants_1.MINIMAP_HEIGHT, constants_1.MINIMAP_HEIGHT);
var MinimapContainer = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  width: 100%;\n  position: relative;\n  left: 0;\n"], ["\n  height: ", "px;\n  width: 100%;\n  position: relative;\n  left: 0;\n"])), constants_1.MINIMAP_HEIGHT);
var ViewHandleContainer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n"])), constants_1.MINIMAP_HEIGHT);
var ViewHandleLine = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  width: 2px;\n  background-color: ", ";\n"], ["\n  height: ", "px;\n  width: 2px;\n  background-color: ", ";\n"])), constants_1.MINIMAP_HEIGHT - constants_1.VIEW_HANDLE_HEIGHT, function (p) { return p.theme.textColor; });
var ViewHandle = styled_1.default('div')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  background-color: ", ";\n  cursor: col-resize;\n  width: 8px;\n  height: ", "px;\n  bottom: 0;\n  left: -3px;\n"], ["\n  position: absolute;\n  background-color: ", ";\n  cursor: col-resize;\n  width: 8px;\n  height: ", "px;\n  bottom: 0;\n  left: -3px;\n"])), function (p) { return p.theme.textColor; }, constants_1.VIEW_HANDLE_HEIGHT);
var Fog = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  opacity: 0.1;\n  position: absolute;\n  top: 0;\n"], ["\n  background-color: ", ";\n  opacity: 0.1;\n  position: absolute;\n  top: 0;\n"])), function (p) { return p.theme.textColor; });
var MinimapSpanBar = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  height: 2px;\n  min-height: 2px;\n  max-height: 2px;\n  margin: 2px 0;\n  min-width: 1px;\n  border-radius: 1px;\n"], ["\n  position: relative;\n  height: 2px;\n  min-height: 2px;\n  max-height: 2px;\n  margin: 2px 0;\n  min-width: 1px;\n  border-radius: 1px;\n"])));
var BackgroundSlider = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var CursorGuide = styled_1.default('div')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n"], ["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n"])), function (p) { return p.theme.red300; });
var Handle = function (_a) {
    var left = _a.left, onMouseDown = _a.onMouseDown, isDragging = _a.isDragging;
    return (<ViewHandleContainer style={{
            left: utils_1.toPercent(left),
        }}>
    <ViewHandleLine />
    <ViewHandle data-ignore="true" onMouseDown={onMouseDown} isDragging={isDragging} style={{
            height: constants_1.VIEW_HANDLE_HEIGHT + "px",
        }}/>
  </ViewHandleContainer>);
};
var WindowSelection = styled_1.default('div')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  background-color: ", ";\n  opacity: 0.1;\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  background-color: ", ";\n  opacity: 0.1;\n"])), constants_1.MINIMAP_HEIGHT, function (p) { return p.theme.textColor; });
exports.SecondaryHeader = styled_1.default('div')(templateObject_17 || (templateObject_17 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: ", "px;\n  left: 0;\n  height: ", "px;\n  width: 100%;\n  background-color: ", ";\n  display: flex;\n  border-top: 1px solid ", ";\n  overflow: hidden;\n"], ["\n  position: absolute;\n  top: ", "px;\n  left: 0;\n  height: ", "px;\n  width: 100%;\n  background-color: ", ";\n  display: flex;\n  border-top: 1px solid ", ";\n  overflow: hidden;\n"])), constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT, constants_1.TIME_AXIS_HEIGHT, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var OperationsBreakdown = styled_1.default('div')(templateObject_18 || (templateObject_18 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  overflow: hidden;\n"], ["\n  height: ", "px;\n  position: absolute;\n  left: 0;\n  top: 0;\n  overflow: hidden;\n"])), constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT);
var RightSidePane = styled_1.default('div')(templateObject_19 || (templateObject_19 = tslib_1.__makeTemplateObject(["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n"], ["\n  height: ", "px;\n  position: absolute;\n  top: 0;\n"])), constants_1.MINIMAP_HEIGHT + constants_1.TIME_AXIS_HEIGHT);
exports.default = TraceViewHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19;
//# sourceMappingURL=header.jsx.map