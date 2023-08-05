Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var discoverFeature_1 = tslib_1.__importDefault(require("app/components/discover/discoverFeature"));
var discoverButton_1 = tslib_1.__importDefault(require("app/components/discoverButton"));
var AnchorLinkManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/anchorLinkManager"));
var DividerHandlerManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/dividerHandlerManager"));
var ScrollbarManager = tslib_1.__importStar(require("app/components/events/interfaces/spans/scrollbarManager"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var messageRow_1 = require("app/components/performance/waterfall/messageRow");
var miniHeader_1 = require("app/components/performance/waterfall/miniHeader");
var utils_1 = require("app/components/performance/waterfall/utils");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var createFuzzySearch_1 = require("app/utils/createFuzzySearch");
var formatters_1 = require("app/utils/formatters");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var utils_2 = require("app/utils/performance/quickTrace/utils");
var breadcrumb_1 = tslib_1.__importDefault(require("app/views/performance/breadcrumb"));
var styles_1 = require("app/views/performance/transactionDetails/styles");
var styles_2 = require("./styles");
var transactionGroup_1 = tslib_1.__importDefault(require("./transactionGroup"));
var utils_3 = require("./utils");
var TraceDetailsContent = /** @class */ (function (_super) {
    tslib_1.__extends(TraceDetailsContent, _super);
    function TraceDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchQuery: undefined,
            filteredTransactionIds: undefined,
        };
        _this.traceViewRef = React.createRef();
        _this.virtualScrollbarContainerRef = React.createRef();
        _this.handleTransactionFilter = function (searchQuery) {
            _this.setState({ searchQuery: searchQuery || undefined }, _this.filterTransactions);
        };
        _this.filterTransactions = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var traces, _a, filteredTransactionIds, searchQuery, transformed, fuse, fuseMatches, idMatches;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        traces = this.props.traces;
                        _a = this.state, filteredTransactionIds = _a.filteredTransactionIds, searchQuery = _a.searchQuery;
                        if (!searchQuery || traces === null || traces.length <= 0) {
                            if (filteredTransactionIds !== undefined) {
                                this.setState({
                                    filteredTransactionIds: undefined,
                                });
                            }
                            return [2 /*return*/];
                        }
                        transformed = traces.flatMap(function (trace) {
                            return utils_2.reduceTrace(trace, function (acc, transaction) {
                                var indexed = [
                                    transaction['transaction.op'],
                                    transaction.transaction,
                                    transaction.project_slug,
                                ];
                                acc.push({
                                    transaction: transaction,
                                    indexed: indexed,
                                });
                                return acc;
                            }, []);
                        });
                        return [4 /*yield*/, createFuzzySearch_1.createFuzzySearch(transformed, {
                                keys: ['indexed'],
                                includeMatches: true,
                                threshold: 0.6,
                                location: 0,
                                distance: 100,
                                maxPatternLength: 32,
                            })];
                    case 1:
                        fuse = _b.sent();
                        fuseMatches = fuse
                            .search(searchQuery)
                            /**
                             * Sometimes, there can be matches that don't include any
                             * indices. These matches are often noise, so exclude them.
                             */
                            .filter(function (_a) {
                            var matches = _a.matches;
                            return matches.length;
                        })
                            .map(function (_a) {
                            var item = _a.item;
                            return item.transaction.event_id;
                        });
                        idMatches = traces
                            .flatMap(function (trace) {
                            return utils_2.filterTrace(trace, function (_a) {
                                var event_id = _a.event_id, span_id = _a.span_id;
                                return event_id.includes(searchQuery) || span_id.includes(searchQuery);
                            });
                        })
                            .map(function (transaction) { return transaction.event_id; });
                        this.setState({
                            filteredTransactionIds: new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fuseMatches)), tslib_1.__read(idMatches))),
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.isTransactionVisible = function (transaction) {
            var filteredTransactionIds = _this.state.filteredTransactionIds;
            return filteredTransactionIds
                ? filteredTransactionIds.has(transaction.event_id)
                : true;
        };
        return _this;
    }
    TraceDetailsContent.prototype.renderTraceLoading = function () {
        return <loadingIndicator_1.default />;
    };
    TraceDetailsContent.prototype.renderTraceRequiresDateRangeSelection = function () {
        return <loadingError_1.default message={locale_1.t('Trace view requires a date range selection.')}/>;
    };
    TraceDetailsContent.prototype.renderTraceNotFound = function () {
        return <loadingError_1.default message={locale_1.t('The trace you are looking for was not found.')}/>;
    };
    TraceDetailsContent.prototype.renderSearchBar = function () {
        return (<styles_2.SearchContainer>
        <styles_2.StyledSearchBar defaultQuery="" query={this.state.searchQuery || ''} placeholder={locale_1.t('Search for transactions')} onSearch={this.handleTransactionFilter}/>
      </styles_2.SearchContainer>);
    };
    TraceDetailsContent.prototype.renderTraceHeader = function (traceInfo) {
        var _a, _b, _c;
        var meta = this.props.meta;
        return (<styles_2.TraceDetailHeader>
        <guideAnchor_1.default target="trace_view_guide_breakdown">
          <styles_1.MetaData headingText={locale_1.t('Event Breakdown')} tooltipText={locale_1.t('The number of transactions and errors there are in this trace.')} bodyText={locale_1.tct('[transactions]  |  [errors]', {
                transactions: locale_1.tn('%s Transaction', '%s Transactions', (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : traceInfo.transactions.size),
                errors: locale_1.tn('%s Error', '%s Errors', (_b = meta === null || meta === void 0 ? void 0 : meta.errors) !== null && _b !== void 0 ? _b : traceInfo.errors.size),
            })} subtext={locale_1.tn('Across %s project', 'Across %s projects', (_c = meta === null || meta === void 0 ? void 0 : meta.projects) !== null && _c !== void 0 ? _c : traceInfo.projects.size)}/>
        </guideAnchor_1.default>
        <styles_1.MetaData headingText={locale_1.t('Total Duration')} tooltipText={locale_1.t('The time elapsed between the start and end of this trace.')} bodyText={formatters_1.getDuration(traceInfo.endTimestamp - traceInfo.startTimestamp, 2, true)} subtext={getDynamicText_1.default({
                value: <timeSince_1.default date={(traceInfo.endTimestamp || 0) * 1000}/>,
                fixed: '5 days ago',
            })}/>
      </styles_2.TraceDetailHeader>);
    };
    TraceDetailsContent.prototype.renderTraceWarnings = function () {
        var traces = this.props.traces;
        var _a = (traces !== null && traces !== void 0 ? traces : []).reduce(function (counts, trace) {
            if (utils_3.isRootTransaction(trace)) {
                counts.roots++;
            }
            else {
                counts.orphans++;
            }
            return counts;
        }, { roots: 0, orphans: 0 }), roots = _a.roots, orphans = _a.orphans;
        var warning = null;
        if (roots === 0 && orphans > 0) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {locale_1.t('A root transaction is missing. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        else if (roots === 1 && orphans > 0) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {locale_1.t('This trace has broken subtraces. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        else if (roots > 1) {
            warning = (<alert_1.default type="info" icon={<icons_1.IconInfo size="sm"/>}>
          <externalLink_1.default href="https://docs.sentry.io/product/performance/trace-view/#multiple-roots">
            {locale_1.t('Multiple root transactions have been found with this trace ID.')}
          </externalLink_1.default>
        </alert_1.default>);
        }
        return warning;
    };
    TraceDetailsContent.prototype.renderInfoMessage = function (_a) {
        var isVisible = _a.isVisible, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove;
        var messages = [];
        if (isVisible) {
            if (numberOfHiddenTransactionsAbove === 1) {
                messages.push(<span key="stuff">
            {locale_1.tct('[numOfTransaction] hidden transaction', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
            else if (numberOfHiddenTransactionsAbove > 1) {
                messages.push(<span key="stuff">
            {locale_1.tct('[numOfTransaction] hidden transactions', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <messageRow_1.MessageRow>{messages}</messageRow_1.MessageRow>;
    };
    TraceDetailsContent.prototype.renderLimitExceededMessage = function (traceInfo) {
        var _a;
        var _b = this.props, traceEventView = _b.traceEventView, organization = _b.organization, meta = _b.meta;
        var count = traceInfo.transactions.size;
        var totalTransactions = (_a = meta === null || meta === void 0 ? void 0 : meta.transactions) !== null && _a !== void 0 ? _a : count;
        if (totalTransactions === null || count >= totalTransactions) {
            return null;
        }
        var target = traceEventView.getResultsViewUrlTarget(organization.slug);
        return (<messageRow_1.MessageRow>
        {locale_1.tct('Limited to a view of [count] transactions. To view the full list, [discover].', {
                count: count,
                discover: (<discoverFeature_1.default>
                {function (_a) {
                        var hasFeature = _a.hasFeature;
                        return (<link_1.default disabled={!hasFeature} to={target}>
                    Open in Discover
                  </link_1.default>);
                    }}
              </discoverFeature_1.default>),
            })}
      </messageRow_1.MessageRow>);
    };
    TraceDetailsContent.prototype.renderTransaction = function (transaction, _a) {
        var _this = this;
        var continuingDepths = _a.continuingDepths, isOrphan = _a.isOrphan, isLast = _a.isLast, index = _a.index, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove, traceInfo = _a.traceInfo, hasGuideAnchor = _a.hasGuideAnchor;
        var _b = this.props, location = _b.location, organization = _b.organization;
        var children = transaction.children, eventId = transaction.event_id;
        // Add 1 to the generation to make room for the "root trace"
        var generation = transaction.generation + 1;
        var isVisible = this.isTransactionVisible(transaction);
        var accumulated = children.reduce(function (acc, child, idx) {
            var isLastChild = idx === children.length - 1;
            var hasChildren = child.children.length > 0;
            var result = _this.renderTransaction(child, {
                continuingDepths: !isLastChild && hasChildren
                    ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(continuingDepths)), [{ depth: generation, isOrphanDepth: isOrphan }]) : continuingDepths,
                isOrphan: isOrphan,
                isLast: isLastChild,
                index: acc.lastIndex + 1,
                numberOfHiddenTransactionsAbove: acc.numberOfHiddenTransactionsAbove,
                traceInfo: traceInfo,
                hasGuideAnchor: false,
            });
            acc.lastIndex = result.lastIndex;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.renderedChildren.push(result.transactionGroup);
            return acc;
        }, {
            renderedChildren: [],
            lastIndex: index,
            numberOfHiddenTransactionsAbove: isVisible
                ? 0
                : numberOfHiddenTransactionsAbove + 1,
        });
        return {
            transactionGroup: (<React.Fragment key={eventId}>
          {this.renderInfoMessage({
                    isVisible: isVisible,
                    numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                })}
          <transactionGroup_1.default location={location} organization={organization} traceInfo={traceInfo} transaction={tslib_1.__assign(tslib_1.__assign({}, transaction), { generation: generation })} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} index={index} isVisible={isVisible} hasGuideAnchor={hasGuideAnchor} renderedChildren={accumulated.renderedChildren} barColour={utils_1.pickBarColour(transaction['transaction.op'])}/>
        </React.Fragment>),
            lastIndex: accumulated.lastIndex,
            numberOfHiddenTransactionsAbove: accumulated.numberOfHiddenTransactionsAbove,
        };
    };
    TraceDetailsContent.prototype.renderTraceView = function (traceInfo) {
        var _this = this;
        var _a;
        var sentryTransaction = (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
        var sentrySpan = sentryTransaction === null || sentryTransaction === void 0 ? void 0 : sentryTransaction.startChild({
            op: 'trace.render',
            description: 'trace-view-content',
        });
        var _b = this.props, location = _b.location, organization = _b.organization, traces = _b.traces, traceSlug = _b.traceSlug;
        if (traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        var accumulator = {
            index: 1,
            numberOfHiddenTransactionsAbove: 0,
            traceInfo: traceInfo,
            transactionGroups: [],
        };
        var _c = traces.reduce(function (acc, trace, index) {
            var isLastTransaction = index === traces.length - 1;
            var hasChildren = trace.children.length > 0;
            var isNextChildOrphaned = !isLastTransaction && traces[index + 1].parent_span_id !== null;
            var result = _this.renderTransaction(trace, tslib_1.__assign(tslib_1.__assign({}, acc), { 
                // if the root of a subtrace has a parent_span_idk, then it must be an orphan
                isOrphan: !utils_3.isRootTransaction(trace), isLast: isLastTransaction, continuingDepths: !isLastTransaction && hasChildren
                    ? [{ depth: 0, isOrphanDepth: isNextChildOrphaned }]
                    : [], hasGuideAnchor: index === 0 }));
            acc.index = result.lastIndex + 1;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.transactionGroups.push(result.transactionGroup);
            return acc;
        }, accumulator), transactionGroups = _c.transactionGroups, numberOfHiddenTransactionsAbove = _c.numberOfHiddenTransactionsAbove;
        var traceView = (<styles_2.TraceDetailBody>
        <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
          <DividerHandlerManager.Consumer>
            {function (_a) {
                var dividerPosition = _a.dividerPosition;
                return (<ScrollbarManager.Provider dividerPosition={dividerPosition} interactiveLayerRef={_this.virtualScrollbarContainerRef}>
                <styles_2.StyledPanel>
                  <styles_2.TraceViewHeaderContainer>
                    <ScrollbarManager.Consumer>
                      {function (_a) {
                        var virtualScrollbarRef = _a.virtualScrollbarRef, scrollBarAreaRef = _a.scrollBarAreaRef, onDragStart = _a.onDragStart, onScroll = _a.onScroll;
                        return (<miniHeader_1.ScrollbarContainer ref={_this.virtualScrollbarContainerRef} style={{
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
                  </styles_2.TraceViewHeaderContainer>
                  <styles_2.TraceViewContainer ref={_this.traceViewRef}>
                    <AnchorLinkManager.Provider>
                      <transactionGroup_1.default location={location} organization={organization} traceInfo={traceInfo} transaction={{
                        traceSlug: traceSlug,
                        generation: 0,
                        'transaction.duration': traceInfo.endTimestamp - traceInfo.startTimestamp,
                        children: traces,
                        start_timestamp: traceInfo.startTimestamp,
                        timestamp: traceInfo.endTimestamp,
                    }} continuingDepths={[]} isOrphan={false} isLast={false} index={0} isVisible hasGuideAnchor={false} renderedChildren={transactionGroups} barColour={utils_1.pickBarColour('')}/>
                    </AnchorLinkManager.Provider>
                    {_this.renderInfoMessage({
                        isVisible: true,
                        numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                    })}
                    {_this.renderLimitExceededMessage(traceInfo)}
                  </styles_2.TraceViewContainer>
                </styles_2.StyledPanel>
              </ScrollbarManager.Provider>);
            }}
          </DividerHandlerManager.Consumer>
        </DividerHandlerManager.Provider>
      </styles_2.TraceDetailBody>);
        sentrySpan === null || sentrySpan === void 0 ? void 0 : sentrySpan.finish();
        return traceView;
    };
    TraceDetailsContent.prototype.renderContent = function () {
        var _a = this.props, dateSelected = _a.dateSelected, isLoading = _a.isLoading, error = _a.error, traces = _a.traces;
        if (!dateSelected) {
            return this.renderTraceRequiresDateRangeSelection();
        }
        else if (isLoading) {
            return this.renderTraceLoading();
        }
        else if (error !== null || traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        else {
            var traceInfo = utils_3.getTraceInfo(traces);
            return (<React.Fragment>
          {this.renderTraceWarnings()}
          {this.renderTraceHeader(traceInfo)}
          {this.renderSearchBar()}
          {this.renderTraceView(traceInfo)}
        </React.Fragment>);
        }
    };
    TraceDetailsContent.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, traceEventView = _a.traceEventView, traceSlug = _a.traceSlug;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <breadcrumb_1.default organization={organization} location={location} traceSlug={traceSlug}/>
            <Layout.Title data-test-id="trace-header">
              {locale_1.t('Trace ID: %s', traceSlug)}
            </Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <buttonBar_1.default gap={1}>
              <discoverButton_1.default to={traceEventView.getResultsViewUrlTarget(organization.slug)}>
                Open in Discover
              </discoverButton_1.default>
            </buttonBar_1.default>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>{this.renderContent()}</Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return TraceDetailsContent;
}(React.Component));
exports.default = TraceDetailsContent;
//# sourceMappingURL=content.jsx.map