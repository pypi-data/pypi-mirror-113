Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var AnchorLinkManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/anchorLinkManager"));
var DividerHandlerManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/dividerHandlerManager"));
var ScrollbarManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/scrollbarManager"));
var constants_1 = require("app/components/performance/waterfall/constants");
var row_1 = require("app/components/performance/waterfall/row");
var rowBar_1 = require("app/components/performance/waterfall/rowBar");
var rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
var rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
var treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
var utils_1 = require("app/components/performance/waterfall/utils");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var utils_2 = require("app/utils/performance/quickTrace/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var styles_1 = require("./styles");
var transactionDetail_1 = tslib_1.__importDefault(require("./transactionDetail"));
var MARGIN_LEFT = 0;
var TransactionBar = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionBar, _super);
    function TransactionBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.transactionRowDOMRef = React.createRef();
        _this.toggleDisplayDetail = function () {
            var transaction = _this.props.transaction;
            if (utils_2.isTraceFullDetailed(transaction)) {
                _this.setState(function (state) { return ({
                    showDetail: !state.showDetail,
                }); });
            }
        };
        _this.scrollIntoView = function () {
            var element = _this.transactionRowDOMRef.current;
            if (!element) {
                return;
            }
            var boundingRect = element.getBoundingClientRect();
            var offset = boundingRect.top + window.scrollY;
            _this.setState({ showDetail: true }, function () { return window.scrollTo(0, offset); });
        };
        return _this;
    }
    TransactionBar.prototype.getCurrentOffset = function () {
        var transaction = this.props.transaction;
        var generation = transaction.generation;
        return getOffset(generation);
    };
    TransactionBar.prototype.renderConnector = function (hasToggle) {
        var _a = this.props, continuingDepths = _a.continuingDepths, isExpanded = _a.isExpanded, isOrphan = _a.isOrphan, isLast = _a.isLast, transaction = _a.transaction;
        var generation = transaction.generation;
        var eventId = utils_2.isTraceFullDetailed(transaction)
            ? transaction.event_id
            : transaction.traceSlug;
        if (generation === 0) {
            if (hasToggle) {
                return (<treeConnector_1.ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingDepths.map(function (_a) {
            var depth = _a.depth, isOrphanDepth = _a.isOrphanDepth;
            if (generation - depth <= 1) {
                // If the difference is less than or equal to 1, then it means that the continued
                // bar is from its direct parent. In this case, do not render a connector bar
                // because the tree connector below will suffice.
                return null;
            }
            var left = -1 * getOffset(generation - depth - 1) - 1;
            return (<treeConnector_1.ConnectorBar style={{ left: left }} key={eventId + "-" + depth} orphanBranch={isOrphanDepth}/>);
        });
        if (hasToggle && isExpanded) {
            connectorBars.push(<treeConnector_1.ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? "-" + constants_1.ROW_HEIGHT / 2 + "px" : '0',
                    top: 'auto',
                }} key={eventId + "-last"} orphanBranch={false}/>);
        }
        return (<treeConnector_1.TreeConnector isLast={isLast} hasToggler={hasToggle} orphanBranch={isOrphan}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    };
    TransactionBar.prototype.renderToggle = function (errored) {
        var _a = this.props, isExpanded = _a.isExpanded, transaction = _a.transaction, toggleExpandedState = _a.toggleExpandedState;
        var children = transaction.children, generation = transaction.generation;
        var left = this.getCurrentOffset();
        if (children.length <= 0) {
            return (<treeConnector_1.TreeToggleContainer style={{ left: left + "px" }}>
          {this.renderConnector(false)}
        </treeConnector_1.TreeToggleContainer>);
        }
        var isRoot = generation === 0;
        return (<treeConnector_1.TreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderConnector(true)}
        <treeConnector_1.TreeToggle disabled={isRoot} isExpanded={isExpanded} errored={errored} onClick={function (event) {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                toggleExpandedState();
            }}>
          <count_1.default value={children.length}/>
          {!isRoot && (<div>
              <treeConnector_1.StyledIconChevron direction={isExpanded ? 'up' : 'down'}/>
            </div>)}
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    };
    TransactionBar.prototype.renderTitle = function (scrollbarManagerChildrenProps) {
        var generateContentSpanBarRef = scrollbarManagerChildrenProps.generateContentSpanBarRef;
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var left = this.getCurrentOffset();
        var errored = utils_2.isTraceFullDetailed(transaction)
            ? transaction.errors.length > 0
            : false;
        var content = utils_2.isTraceFullDetailed(transaction) ? (<React.Fragment>
        <projects_1.default orgId={organization.slug} slugs={[transaction.project_slug]}>
          {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === transaction.project_slug; });
                return (<tooltip_1.default title={transaction.project_slug}>
                <styles_1.StyledProjectBadge project={project ? project : { slug: transaction.project_slug }} avatarSize={16} hideName/>
              </tooltip_1.default>);
            }}
        </projects_1.default>
        <rowTitle_1.RowTitleContent errored={errored}>
          <strong>
            {transaction['transaction.op']}
            {' \u2014 '}
          </strong>
          {transaction.transaction}
        </rowTitle_1.RowTitleContent>
      </React.Fragment>) : (<rowTitle_1.RowTitleContent errored={false}>
        <strong>{'Trace \u2014 '}</strong>
        {transaction.traceSlug}
      </rowTitle_1.RowTitleContent>);
        return (<rowTitle_1.RowTitleContainer ref={generateContentSpanBarRef()}>
        {this.renderToggle(errored)}
        <rowTitle_1.RowTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          {content}
        </rowTitle_1.RowTitle>
      </rowTitle_1.RowTitleContainer>);
    };
    TransactionBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
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
    TransactionBar.prototype.renderGhostDivider = function (dividerHandlerChildrenProps) {
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        return (<rowDivider_1.DividerLineGhostContainer style={{
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
      </rowDivider_1.DividerLineGhostContainer>);
    };
    TransactionBar.prototype.renderErrorBadge = function () {
        var transaction = this.props.transaction;
        if (!utils_2.isTraceFullDetailed(transaction) || !transaction.errors.length) {
            return null;
        }
        return <rowDivider_1.ErrorBadge />;
    };
    TransactionBar.prototype.renderRectangle = function () {
        var _a = this.props, transaction = _a.transaction, traceInfo = _a.traceInfo, barColour = _a.barColour;
        var showDetail = this.state.showDetail;
        // Use 1 as the difference in the event that startTimestamp === endTimestamp
        var delta = Math.abs(traceInfo.endTimestamp - traceInfo.startTimestamp) || 1;
        var startPosition = Math.abs(transaction.start_timestamp - traceInfo.startTimestamp);
        var startPercentage = startPosition / delta;
        var duration = Math.abs(transaction.timestamp - transaction.start_timestamp);
        var widthPercentage = duration / delta;
        return (<rowBar_1.RowRectangle spanBarHatch={false} style={{
                backgroundColor: barColour,
                left: "min(" + utils_1.toPercent(startPercentage || 0) + ", calc(100% - 1px))",
                width: utils_1.toPercent(widthPercentage || 0),
            }}>
        <rowBar_1.DurationPill durationDisplay={utils_1.getDurationDisplay({
                left: startPercentage,
                width: widthPercentage,
            })} showDetail={showDetail} spanBarHatch={false}>
          {utils_1.getHumanDuration(duration)}
        </rowBar_1.DurationPill>
      </rowBar_1.RowRectangle>);
    };
    TransactionBar.prototype.renderHeader = function (_a) {
        var dividerHandlerChildrenProps = _a.dividerHandlerChildrenProps, scrollbarManagerChildrenProps = _a.scrollbarManagerChildrenProps;
        var _b = this.props, hasGuideAnchor = _b.hasGuideAnchor, index = _b.index;
        var showDetail = this.state.showDetail;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
        return (<row_1.RowCellContainer showDetail={showDetail}>
        <row_1.RowCell data-test-id="transaction-row-title" data-type="span-row-cell" style={{
                width: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <guideAnchor_1.default target="trace_view_guide_row" disabled={!hasGuideAnchor}>
            {this.renderTitle(scrollbarManagerChildrenProps)}
          </guideAnchor_1.default>
        </row_1.RowCell>
        <rowDivider_1.DividerContainer>
          {this.renderDivider(dividerHandlerChildrenProps)}
          {this.renderErrorBadge()}
        </rowDivider_1.DividerContainer>
        <row_1.RowCell data-test-id="transaction-row-duration" data-type="span-row-cell" showStriping={index % 2 !== 0} style={{
                width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          <guideAnchor_1.default target="trace_view_guide_row_details" disabled={!hasGuideAnchor}>
            {this.renderRectangle()}
          </guideAnchor_1.default>
        </row_1.RowCell>
        {!showDetail && this.renderGhostDivider(dividerHandlerChildrenProps)}
      </row_1.RowCellContainer>);
    };
    TransactionBar.prototype.renderDetail = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, isVisible = _a.isVisible, transaction = _a.transaction;
        var showDetail = this.state.showDetail;
        return (<AnchorLinkManager.Consumer>
        {function (_a) {
                var registerScrollFn = _a.registerScrollFn, scrollToHash = _a.scrollToHash;
                if (!utils_2.isTraceFullDetailed(transaction)) {
                    return null;
                }
                registerScrollFn("#txn-" + transaction.event_id, _this.scrollIntoView);
                if (!isVisible || !showDetail) {
                    return null;
                }
                return (<transactionDetail_1.default location={location} organization={organization} transaction={transaction} scrollToHash={scrollToHash}/>);
            }}
      </AnchorLinkManager.Consumer>);
    };
    TransactionBar.prototype.render = function () {
        var _this = this;
        var _a = this.props, isVisible = _a.isVisible, transaction = _a.transaction;
        var showDetail = this.state.showDetail;
        return (<row_1.Row ref={this.transactionRowDOMRef} visible={isVisible} showBorder={showDetail} cursor={utils_2.isTraceFullDetailed(transaction) ? 'pointer' : 'default'}>
        <ScrollbarManager.Consumer>
          {function (scrollbarManagerChildrenProps) { return (<DividerHandlerManager.Consumer>
              {function (dividerHandlerChildrenProps) {
                    return _this.renderHeader({
                        dividerHandlerChildrenProps: dividerHandlerChildrenProps,
                        scrollbarManagerChildrenProps: scrollbarManagerChildrenProps,
                    });
                }}
            </DividerHandlerManager.Consumer>); }}
        </ScrollbarManager.Consumer>
        {this.renderDetail()}
      </row_1.Row>);
    };
    return TransactionBar;
}(React.Component));
function getOffset(generation) {
    return generation * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
}
exports.default = TransactionBar;
//# sourceMappingURL=transactionBar.jsx.map