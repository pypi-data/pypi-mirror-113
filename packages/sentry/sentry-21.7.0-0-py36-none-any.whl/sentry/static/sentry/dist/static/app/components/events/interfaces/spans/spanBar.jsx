Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("intersection-observer"); // this is a polyfill
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var featureBadge_1 = tslib_1.__importDefault(require("app/components/featureBadge"));
var constants_1 = require("app/components/performance/waterfall/constants");
var messageRow_1 = require("app/components/performance/waterfall/messageRow");
var row_1 = require("app/components/performance/waterfall/row");
var rowBar_1 = require("app/components/performance/waterfall/rowBar");
var rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
var rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
var treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
var utils_1 = require("app/components/performance/waterfall/utils");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var urls_1 = require("app/utils/discover/urls");
var QuickTraceContext = tslib_1.__importStar(require("app/utils/performance/quickTrace/quickTraceContext"));
var utils_3 = require("app/utils/performance/quickTrace/utils");
var AnchorLinkManager = tslib_1.__importStar(require("./anchorLinkManager"));
var constants_2 = require("./constants");
var CursorGuideHandler = tslib_1.__importStar(require("./cursorGuideHandler"));
var DividerHandlerManager = tslib_1.__importStar(require("./dividerHandlerManager"));
var ScrollbarManager = tslib_1.__importStar(require("./scrollbarManager"));
var spanDetail_1 = tslib_1.__importDefault(require("./spanDetail"));
var utils_4 = require("./utils");
// TODO: maybe use babel-plugin-preval
// for (let i = 0; i <= 1.0; i += 0.01) {
//   INTERSECTION_THRESHOLDS.push(i);
// }
var INTERSECTION_THRESHOLDS = [
    0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14,
    0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29,
    0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44,
    0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59,
    0.6, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.7, 0.71, 0.72, 0.73, 0.74,
    0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89,
    0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0,
];
var MARGIN_LEFT = 0;
var SpanBar = /** @class */ (function (_super) {
    tslib_1.__extends(SpanBar, _super);
    function SpanBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.spanRowDOMRef = React.createRef();
        _this.intersectionObserver = void 0;
        _this.zoomLevel = 1; // assume initial zoomLevel is 100%
        _this._mounted = false;
        _this.toggleDisplayDetail = function () {
            _this.setState(function (state) { return ({
                showDetail: !state.showDetail,
            }); });
        };
        _this.scrollIntoView = function () {
            var element = _this.spanRowDOMRef.current;
            if (!element) {
                return;
            }
            var boundingRect = element.getBoundingClientRect();
            var offset = boundingRect.top + window.scrollY - constants_2.MINIMAP_CONTAINER_HEIGHT;
            _this.setState({ showDetail: true }, function () { return window.scrollTo(0, offset); });
        };
        return _this;
    }
    SpanBar.prototype.componentDidMount = function () {
        this._mounted = true;
        if (this.spanRowDOMRef.current) {
            this.connectObservers();
        }
    };
    SpanBar.prototype.componentWillUnmount = function () {
        this._mounted = false;
        this.disconnectObservers();
    };
    SpanBar.prototype.renderDetail = function (_a) {
        var _this = this;
        var isVisible = _a.isVisible, transactions = _a.transactions, errors = _a.errors;
        var _b = this.props, span = _b.span, organization = _b.organization, isRoot = _b.isRoot, trace = _b.trace, event = _b.event;
        return (<AnchorLinkManager.Consumer>
        {function (_a) {
                var registerScrollFn = _a.registerScrollFn, scrollToHash = _a.scrollToHash;
                if (!utils_4.isGapSpan(span)) {
                    registerScrollFn("#span-" + span.span_id, _this.scrollIntoView);
                }
                if (!_this.state.showDetail || !isVisible) {
                    return null;
                }
                return (<spanDetail_1.default span={span} organization={organization} event={event} isRoot={!!isRoot} trace={trace} childTransactions={transactions} relatedErrors={errors} scrollToHash={scrollToHash}/>);
            }}
      </AnchorLinkManager.Consumer>);
    };
    SpanBar.prototype.getBounds = function () {
        var _a = this.props, event = _a.event, span = _a.span, generateBounds = _a.generateBounds;
        var bounds = generateBounds({
            startTimestamp: span.start_timestamp,
            endTimestamp: span.timestamp,
        });
        var shouldHideSpanWarnings = utils_4.isEventFromBrowserJavaScriptSDK(event);
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL': {
                return {
                    warning: locale_1.t('Trace times are equal'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'INVALID_VIEW_WINDOW': {
                return {
                    warning: locale_1.t('Invalid view window'),
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                var warning = shouldHideSpanWarnings &&
                    'op' in span &&
                    span.op &&
                    utils_4.durationlessBrowserOps.includes(span.op)
                    ? void 0
                    : locale_1.t('Equal start and end times');
                return {
                    warning: warning,
                    left: bounds.start,
                    width: 0.00001,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_REVERSED': {
                return {
                    warning: locale_1.t('Reversed start and end times'),
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_STABLE': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            default: {
                var _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    };
    SpanBar.prototype.renderMeasurements = function () {
        var _a = this.props, event = _a.event, generateBounds = _a.generateBounds;
        if (this.state.showDetail) {
            return null;
        }
        var measurements = utils_4.getMeasurements(event);
        return (<React.Fragment>
        {Array.from(measurements).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], verticalMark = _b[1];
                var bounds = utils_4.getMeasurementBounds(timestamp, generateBounds);
                var shouldDisplay = utils_2.defined(bounds.left) && utils_2.defined(bounds.width);
                if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                    return null;
                }
                return (<MeasurementMarker key={String(timestamp)} style={{
                        left: "clamp(0%, " + utils_1.toPercent(bounds.left || 0) + ", calc(100% - 1px))",
                    }} failedThreshold={verticalMark.failedThreshold}/>);
            })}
      </React.Fragment>);
    };
    SpanBar.prototype.renderSpanTreeConnector = function (_a) {
        var hasToggler = _a.hasToggler;
        var _b = this.props, isLast = _b.isLast, isRoot = _b.isRoot, spanTreeDepth = _b.treeDepth, continuingTreeDepths = _b.continuingTreeDepths, span = _b.span, showSpanTree = _b.showSpanTree;
        var spanID = utils_4.getSpanID(span);
        if (isRoot) {
            if (hasToggler) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} key={spanID + "-last"} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingTreeDepths.map(function (treeDepth) {
            var depth = utils_4.unwrapTreeDepth(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            var left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left: left }} key={spanID + "-" + depth} orphanBranch={utils_4.isOrphanTreeDepth(treeDepth)}/>);
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
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggler} orphanBranch={utils_4.isOrphanSpan(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    };
    SpanBar.prototype.renderSpanTreeToggler = function (_a) {
        var _this = this;
        var left = _a.left, errored = _a.errored;
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
        <treeConnector_1.TreeToggle disabled={!!isRoot} isExpanded={showSpanTree} errored={errored} onClick={function (event) {
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
    SpanBar.prototype.renderTitle = function (scrollbarManagerChildrenProps, errors) {
        var _a;
        var generateContentSpanBarRef = scrollbarManagerChildrenProps.generateContentSpanBarRef;
        var _b = this.props, span = _b.span, treeDepth = _b.treeDepth;
        var operationName = utils_4.getSpanOperation(span) ? (<strong>
        {utils_4.getSpanOperation(span)}
        {' \u2014 '}
      </strong>) : ('');
        var description = (_a = span === null || span === void 0 ? void 0 : span.description) !== null && _a !== void 0 ? _a : utils_4.getSpanID(span);
        var left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
        var errored = Boolean(errors && errors.length > 0);
        return (<rowTitle_1.RowTitleContainer data-debug-id="SpanBarTitleContainer" ref={generateContentSpanBarRef()}>
        {this.renderSpanTreeToggler({ left: left, errored: errored })}
        <rowTitle_1.RowTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          <rowTitle_1.RowTitleContent errored={errored}>
            {operationName}
            {description}
          </rowTitle_1.RowTitleContent>
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
    };
    SpanBar.prototype.connectObservers = function () {
        var _this = this;
        if (!this.spanRowDOMRef.current) {
            return;
        }
        this.disconnectObservers();
        /**
    
        We track intersections events between the span bar's DOM element
        and the viewport's (root) intersection area. the intersection area is sized to
        exclude the minimap. See below.
    
        By default, the intersection observer's root intersection is the viewport.
        We adjust the margins of this root intersection area to exclude the minimap's
        height. The minimap's height is always fixed.
    
          VIEWPORT (ancestor element used for the intersection events)
        +--+-------------------------+--+
        |  |                         |  |
        |  |       MINIMAP           |  |
        |  |                         |  |
        |  +-------------------------+  |  ^
        |  |                         |  |  |
        |  |       SPANS             |  |  | ROOT
        |  |                         |  |  | INTERSECTION
        |  |                         |  |  | OBSERVER
        |  |                         |  |  | HEIGHT
        |  |                         |  |  |
        |  |                         |  |  |
        |  |                         |  |  |
        |  +-------------------------+  |  |
        |                               |  |
        +-------------------------------+  v
    
         */
        this.intersectionObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!_this._mounted) {
                    return;
                }
                var shouldMoveMinimap = _this.props.trace.numOfSpans > constants_2.NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (!shouldMoveMinimap) {
                    return;
                }
                var spanNumber = _this.props.spanNumber;
                var minimapSlider = document.getElementById('minimap-background-slider');
                if (!minimapSlider) {
                    return;
                }
                // NOTE: THIS IS HACKY.
                //
                // IntersectionObserver.rootMargin is un-affected by the browser's zoom level.
                // The margins of the intersection area needs to be adjusted.
                // Thus, IntersectionObserverEntry.rootBounds may not be what we expect.
                //
                // We address this below.
                //
                // Note that this function was called whenever an intersection event occurred wrt
                // the thresholds.
                //
                if (entry.rootBounds) {
                    // After we create the IntersectionObserver instance with rootMargin set as:
                    // -${MINIMAP_CONTAINER_HEIGHT * this.zoomLevel}px 0px 0px 0px
                    //
                    // we can introspect the rootBounds to infer the zoomlevel.
                    //
                    // we always expect entry.rootBounds.top to equal MINIMAP_CONTAINER_HEIGHT
                    var actualRootTop = Math.ceil(entry.rootBounds.top);
                    if (actualRootTop !== constants_2.MINIMAP_CONTAINER_HEIGHT && actualRootTop > 0) {
                        // we revert the actualRootTop value by the current zoomLevel factor
                        var normalizedActualTop = actualRootTop / _this.zoomLevel;
                        var zoomLevel = constants_2.MINIMAP_CONTAINER_HEIGHT / normalizedActualTop;
                        _this.zoomLevel = zoomLevel;
                        // we reconnect the observers; the callback functions may be invoked
                        _this.connectObservers();
                        // NOTE: since we cannot guarantee that the callback function is invoked on
                        //       the newly connected observers, we continue running this function.
                    }
                }
                // root refers to the root intersection rectangle used for the IntersectionObserver
                var rectRelativeToRoot = entry.boundingClientRect;
                var bottomYCoord = rectRelativeToRoot.y + rectRelativeToRoot.height;
                // refers to if the rect is out of view from the viewport
                var isOutOfViewAbove = rectRelativeToRoot.y < 0 && bottomYCoord < 0;
                if (isOutOfViewAbove) {
                    return;
                }
                var relativeToMinimap = {
                    top: rectRelativeToRoot.y - constants_2.MINIMAP_CONTAINER_HEIGHT,
                    bottom: bottomYCoord - constants_2.MINIMAP_CONTAINER_HEIGHT,
                };
                var rectBelowMinimap = relativeToMinimap.top > 0 && relativeToMinimap.bottom > 0;
                if (rectBelowMinimap) {
                    // if the first span is below the minimap, we scroll the minimap
                    // to the top. this addresses spurious scrolling to the top of the page
                    if (spanNumber <= 1) {
                        minimapSlider.style.top = '0px';
                        return;
                    }
                    return;
                }
                var inAndAboveMinimap = relativeToMinimap.bottom <= 0;
                if (inAndAboveMinimap) {
                    return;
                }
                // invariant: spanNumber >= 1
                var numberOfMovedSpans = spanNumber - 1;
                var totalHeightOfHiddenSpans = numberOfMovedSpans * constants_2.MINIMAP_SPAN_BAR_HEIGHT;
                var currentSpanHiddenRatio = 1 - entry.intersectionRatio;
                var panYPixels = totalHeightOfHiddenSpans + currentSpanHiddenRatio * constants_2.MINIMAP_SPAN_BAR_HEIGHT;
                // invariant: this.props.trace.numOfSpansend - spanNumberToStopMoving + 1 = NUM_OF_SPANS_FIT_IN_MINI_MAP
                var spanNumberToStopMoving = _this.props.trace.numOfSpans + 1 - constants_2.NUM_OF_SPANS_FIT_IN_MINI_MAP;
                if (spanNumber > spanNumberToStopMoving) {
                    // if the last span bar appears on the minimap, we do not want the minimap
                    // to keep panning upwards
                    minimapSlider.style.top = "-" + spanNumberToStopMoving * constants_2.MINIMAP_SPAN_BAR_HEIGHT + "px";
                    return;
                }
                minimapSlider.style.top = "-" + panYPixels + "px";
            });
        }, {
            threshold: INTERSECTION_THRESHOLDS,
            rootMargin: "-" + constants_2.MINIMAP_CONTAINER_HEIGHT * this.zoomLevel + "px 0px 0px 0px",
        });
        this.intersectionObserver.observe(this.spanRowDOMRef.current);
    };
    SpanBar.prototype.disconnectObservers = function () {
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
    };
    SpanBar.prototype.renderCursorGuide = function () {
        return (<CursorGuideHandler.Consumer>
        {function (_a) {
                var showCursorGuide = _a.showCursorGuide, traceViewMouseLeft = _a.traceViewMouseLeft;
                if (!showCursorGuide || !traceViewMouseLeft) {
                    return null;
                }
                return (<CursorGuide style={{
                        left: utils_1.toPercent(traceViewMouseLeft),
                    }}/>);
            }}
      </CursorGuideHandler.Consumer>);
    };
    SpanBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        if (this.state.showDetail) {
            // Mock component to preserve layout spacing
            return (<rowDivider_1.DividerLine showDetail style={{
                    position: 'absolute',
                }}/>);
        }
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<rowDivider_1.DividerLine ref={addDividerLineRef()} style={{
                position: 'absolute',
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
    SpanBar.prototype.getRelatedErrors = function (quickTrace) {
        if (!quickTrace) {
            return null;
        }
        var span = this.props.span;
        var currentEvent = quickTrace.currentEvent;
        if (utils_4.isGapSpan(span) || !currentEvent || !utils_3.isTraceFull(currentEvent)) {
            return null;
        }
        return currentEvent.errors.filter(function (error) { return error.span === span.span_id; });
    };
    SpanBar.prototype.getChildTransactions = function (quickTrace) {
        if (!quickTrace) {
            return null;
        }
        var span = this.props.span;
        var trace = quickTrace.trace;
        if (utils_4.isGapSpan(span) || !trace) {
            return null;
        }
        return trace.filter(function (_a) {
            var parent_span_id = _a.parent_span_id;
            return parent_span_id === span.span_id;
        });
    };
    SpanBar.prototype.renderErrorBadge = function (errors) {
        return (errors === null || errors === void 0 ? void 0 : errors.length) ? <rowDivider_1.ErrorBadge /> : null;
    };
    SpanBar.prototype.renderEmbeddedTransactionsBadge = function (transactions) {
        var _a = this.props, toggleEmbeddedChildren = _a.toggleEmbeddedChildren, organization = _a.organization, showEmbeddedChildren = _a.showEmbeddedChildren;
        if (!organization.features.includes('unified-span-view')) {
            return null;
        }
        if (transactions && transactions.length === 1) {
            var transaction_1 = transactions[0];
            return (<tooltip_1.default title={<span>
              {showEmbeddedChildren
                        ? locale_1.t('This span is showing a direct child. Remove transaction to hide')
                        : locale_1.t('This span has a direct child. Add transaction to view')}
              <featureBadge_1.default type="beta" noTooltip/>
            </span>} position="top" containerDisplayMode="block">
          <rowDivider_1.EmbeddedTransactionBadge expanded={showEmbeddedChildren} onClick={function () {
                    if (toggleEmbeddedChildren) {
                        if (showEmbeddedChildren) {
                            analytics_1.trackAnalyticsEvent({
                                eventKey: 'span_view.embedded_child.hide',
                                eventName: 'Span View: Hide Embedded Transaction',
                                organization_id: parseInt(organization.id, 10),
                            });
                        }
                        else {
                            analytics_1.trackAnalyticsEvent({
                                eventKey: 'span_view.embedded_child.show',
                                eventName: 'Span View: Show Embedded Transaction',
                                organization_id: parseInt(organization.id, 10),
                            });
                        }
                        toggleEmbeddedChildren({
                            orgSlug: organization.slug,
                            eventSlug: urls_1.generateEventSlug({
                                id: transaction_1.event_id,
                                project: transaction_1.project_slug,
                            }),
                        });
                    }
                }}/>
        </tooltip_1.default>);
        }
        return null;
    };
    SpanBar.prototype.renderWarningText = function (_a) {
        var _b = _a === void 0 ? {} : _a, warningText = _b.warningText;
        if (!warningText) {
            return null;
        }
        return (<tooltip_1.default containerDisplayMode="flex" title={warningText}>
        <StyledIconWarning size="xs"/>
      </tooltip_1.default>);
    };
    SpanBar.prototype.renderHeader = function (_a) {
        var _this = this;
        var scrollbarManagerChildrenProps = _a.scrollbarManagerChildrenProps, dividerHandlerChildrenProps = _a.dividerHandlerChildrenProps, errors = _a.errors, transactions = _a.transactions;
        var _b = this.props, span = _b.span, spanBarColour = _b.spanBarColour, spanBarHatch = _b.spanBarHatch, spanNumber = _b.spanNumber;
        var startTimestamp = span.start_timestamp;
        var endTimestamp = span.timestamp;
        var duration = Math.abs(endTimestamp - startTimestamp);
        var durationString = utils_1.getHumanDuration(duration);
        var bounds = this.getBounds();
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        var displaySpanBar = utils_2.defined(bounds.left) && utils_2.defined(bounds.width);
        var durationDisplay = utils_1.getDurationDisplay(bounds);
        return (<row_1.RowCellContainer showDetail={this.state.showDetail}>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} style={{
                width: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          {this.renderTitle(scrollbarManagerChildrenProps, errors)}
        </row_1.RowCell>
        <rowDivider_1.DividerContainer>
          {this.renderDivider(dividerHandlerChildrenProps)}
          {this.renderErrorBadge(errors)}
          {this.renderEmbeddedTransactionsBadge(transactions)}
        </rowDivider_1.DividerContainer>
        <row_1.RowCell data-type="span-row-cell" showDetail={this.state.showDetail} showStriping={spanNumber % 2 !== 0} style={{
                width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
            }} onClick={function () {
                _this.toggleDisplayDetail();
            }}>
          {displaySpanBar && (<rowBar_1.RowRectangle spanBarHatch={!!spanBarHatch} style={{
                    backgroundColor: spanBarColour,
                    left: "min(" + utils_1.toPercent(bounds.left || 0) + ", calc(100% - 1px))",
                    width: utils_1.toPercent(bounds.width || 0),
                }}>
              <rowBar_1.DurationPill durationDisplay={durationDisplay} showDetail={this.state.showDetail} spanBarHatch={!!spanBarHatch}>
                {durationString}
                {this.renderWarningText({ warningText: bounds.warning })}
              </rowBar_1.DurationPill>
            </rowBar_1.RowRectangle>)}
          {this.renderMeasurements()}
          {this.renderCursorGuide()}
        </row_1.RowCell>
        {!this.state.showDetail && (<rowDivider_1.DividerLineGhostContainer style={{
                    width: "calc(" + utils_1.toPercent(dividerPosition) + " + 0.5px)",
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
    SpanBar.prototype.renderEmbeddedChildrenState = function () {
        var fetchEmbeddedChildrenState = this.props.fetchEmbeddedChildrenState;
        switch (fetchEmbeddedChildrenState) {
            case 'loading_embedded_transactions': {
                return (<messageRow_1.MessageRow>
            <span>{locale_1.t('Loading embedded transaction')}</span>
          </messageRow_1.MessageRow>);
            }
            case 'error_fetching_embedded_transactions': {
                return (<messageRow_1.MessageRow>
            <span>{locale_1.t('Error loading embedded transaction')}</span>
          </messageRow_1.MessageRow>);
            }
            default:
                return null;
        }
    };
    SpanBar.prototype.render = function () {
        var _this = this;
        var isCurrentSpanFilteredOut = this.props.isCurrentSpanFilteredOut;
        var bounds = this.getBounds();
        var isSpanVisibleInView = bounds.isSpanVisibleInView;
        var isSpanVisible = isSpanVisibleInView && !isCurrentSpanFilteredOut;
        return (<React.Fragment>
        <row_1.Row ref={this.spanRowDOMRef} visible={isSpanVisible} showBorder={this.state.showDetail} data-test-id="span-row">
          <QuickTraceContext.Consumer>
            {function (quickTrace) {
                var errors = _this.getRelatedErrors(quickTrace);
                var transactions = _this.getChildTransactions(quickTrace);
                return (<React.Fragment>
                  <ScrollbarManager.Consumer>
                    {function (scrollbarManagerChildrenProps) { return (<DividerHandlerManager.Consumer>
                        {function (dividerHandlerChildrenProps) {
                            return _this.renderHeader({
                                dividerHandlerChildrenProps: dividerHandlerChildrenProps,
                                scrollbarManagerChildrenProps: scrollbarManagerChildrenProps,
                                errors: errors,
                                transactions: transactions,
                            });
                        }}
                      </DividerHandlerManager.Consumer>); }}
                  </ScrollbarManager.Consumer>
                  {_this.renderDetail({ isVisible: isSpanVisible, transactions: transactions, errors: errors })}
                </React.Fragment>);
            }}
          </QuickTraceContext.Consumer>
        </row_1.Row>
        {this.renderEmbeddedChildrenState()}
      </React.Fragment>);
    };
    return SpanBar;
}(React.Component));
var CursorGuide = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"], ["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"])), function (p) { return p.theme.red300; });
var MeasurementMarker = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"])), constants_1.ROW_HEIGHT, function (p) { return (p.failedThreshold ? p.theme.red300 : 'black'); }, function (p) { return p.theme.zIndex.traceView.dividerLine; }, function (p) { return p.theme.textColor; });
var StyledIconWarning = styled_1.default(icons_1.IconWarning)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-left: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(0.25), space_1.default(0.25));
exports.default = SpanBar;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=spanBar.jsx.map