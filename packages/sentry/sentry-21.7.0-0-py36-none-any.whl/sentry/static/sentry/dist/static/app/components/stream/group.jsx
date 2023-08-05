Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_STREAM_GROUP_STATS_PERIOD = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var assigneeSelector_1 = tslib_1.__importDefault(require("app/components/assigneeSelector"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var dropdownMenu_1 = tslib_1.__importDefault(require("app/components/dropdownMenu"));
var eventOrGroupExtraDetails_1 = tslib_1.__importDefault(require("app/components/eventOrGroupExtraDetails"));
var eventOrGroupHeader_1 = tslib_1.__importDefault(require("app/components/eventOrGroupHeader"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var utils_1 = require("app/components/organizations/timeRangeSelector/utils");
var panels_1 = require("app/components/panels");
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var progressBar_1 = tslib_1.__importDefault(require("app/components/progressBar"));
var groupChart_1 = tslib_1.__importDefault(require("app/components/stream/groupChart"));
var groupCheckBox_1 = tslib_1.__importDefault(require("app/components/stream/groupCheckBox"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var selectedGroupStore_1 = tslib_1.__importDefault(require("app/stores/selectedGroupStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var callIfFunction_1 = require("app/utils/callIfFunction");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var formatters_1 = require("app/utils/formatters");
var stream_1 = require("app/utils/stream");
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var utils_3 = require("app/views/issueList/utils");
var DiscoveryExclusionFields = [
    'query',
    'status',
    'bookmarked_by',
    'assigned',
    'assigned_to',
    'unassigned',
    'subscribed_by',
    'active_at',
    'first_release',
    'first_seen',
    'is',
    '__text',
];
exports.DEFAULT_STREAM_GROUP_STATS_PERIOD = '24h';
var DEFAULT_DISPLAY = utils_3.IssueDisplayOptions.EVENTS;
var defaultProps = {
    statsPeriod: exports.DEFAULT_STREAM_GROUP_STATS_PERIOD,
    canSelect: true,
    withChart: true,
    useFilteredStats: false,
    useTintRow: true,
    display: DEFAULT_DISPLAY,
    narrowGroups: false,
};
var StreamGroup = /** @class */ (function (_super) {
    tslib_1.__extends(StreamGroup, _super);
    function StreamGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listener = groupStore_1.default.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        _this.trackClick = function () {
            var _a = _this.props, query = _a.query, organization = _a.organization;
            var data = _this.state.data;
            if (query === utils_3.Query.FOR_REVIEW) {
                analytics_1.trackAnalyticsEvent({
                    eventKey: 'inbox_tab.issue_clicked',
                    eventName: 'Clicked Issue from Inbox Tab',
                    organization_id: organization.id,
                    group_id: data.id,
                });
            }
            if (query !== undefined) {
                analytics_1.trackAnalyticsEvent(tslib_1.__assign({ eventKey: 'issues_stream.issue_clicked', eventName: 'Clicked Issue from Issues Stream' }, _this.sharedAnalytics()));
            }
        };
        _this.trackAssign = function (type, _assignee, suggestedAssignee) {
            var query = _this.props.query;
            if (query !== undefined) {
                analytics_1.trackAnalyticsEvent(tslib_1.__assign(tslib_1.__assign({ eventKey: 'issues_stream.issue_assigned', eventName: 'Assigned Issue from Issues Stream' }, _this.sharedAnalytics()), { did_assign_suggestion: !!suggestedAssignee, assigned_suggestion_reason: suggestedAssignee === null || suggestedAssignee === void 0 ? void 0 : suggestedAssignee.suggestedReason, assigned_type: type }));
            }
        };
        _this.toggleSelect = function (evt) {
            var _a, _b, _c;
            var targetElement = evt.target;
            if (((_a = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === 'a') {
                return;
            }
            if (((_b = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _b === void 0 ? void 0 : _b.toLowerCase()) === 'input') {
                return;
            }
            var e = targetElement;
            while (e.parentElement) {
                if (((_c = e === null || e === void 0 ? void 0 : e.tagName) === null || _c === void 0 ? void 0 : _c.toLowerCase()) === 'a') {
                    return;
                }
                e = e.parentElement;
            }
            selectedGroupStore_1.default.toggleSelect(_this.state.data.id);
        };
        return _this;
    }
    StreamGroup.prototype.getInitialState = function () {
        var _a = this.props, id = _a.id, useFilteredStats = _a.useFilteredStats;
        var data = groupStore_1.default.get(id);
        return {
            data: tslib_1.__assign(tslib_1.__assign({}, data), { filtered: useFilteredStats ? data.filtered : null }),
            reviewed: false,
            actionTaken: false,
        };
    };
    StreamGroup.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id ||
            nextProps.useFilteredStats !== this.props.useFilteredStats) {
            var data = groupStore_1.default.get(this.props.id);
            this.setState({
                data: tslib_1.__assign(tslib_1.__assign({}, data), { filtered: nextProps.useFilteredStats ? data.filtered : null }),
            });
        }
    };
    StreamGroup.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextProps.statsPeriod !== this.props.statsPeriod) {
            return true;
        }
        if (!utils_2.valueIsEqual(this.state.data, nextState.data)) {
            return true;
        }
        return false;
    };
    StreamGroup.prototype.componentWillUnmount = function () {
        callIfFunction_1.callIfFunction(this.listener);
    };
    StreamGroup.prototype.onGroupChange = function (itemIds) {
        var _a = this.props, id = _a.id, query = _a.query;
        if (!itemIds.has(id)) {
            return;
        }
        var actionTaken = this.state.data.status !== 'unresolved';
        var data = groupStore_1.default.get(id);
        this.setState(function (state) {
            var _a;
            // When searching is:for_review and the inbox reason is removed
            var reviewed = state.reviewed ||
                (utils_3.isForReviewQuery(query) &&
                    ((_a = state.data.inbox) === null || _a === void 0 ? void 0 : _a.reason) !== undefined &&
                    data.inbox === false);
            return { data: data, reviewed: reviewed, actionTaken: actionTaken };
        });
    };
    /** Shared between two events */
    StreamGroup.prototype.sharedAnalytics = function () {
        var _a;
        var _b = this.props, query = _b.query, organization = _b.organization;
        var data = this.state.data;
        var tab = (_a = utils_3.getTabs(organization).find(function (_a) {
            var _b = tslib_1.__read(_a, 1), tabQuery = _b[0];
            return tabQuery === query;
        })) === null || _a === void 0 ? void 0 : _a[1];
        var owners = (data === null || data === void 0 ? void 0 : data.owners) || [];
        return {
            organization_id: organization.id,
            group_id: data.id,
            tab: (tab === null || tab === void 0 ? void 0 : tab.analyticsName) || 'other',
            was_shown_suggestion: owners.length > 0,
        };
    };
    StreamGroup.prototype.getDiscoverUrl = function (isFiltered) {
        var _a = this.props, organization = _a.organization, query = _a.query, selection = _a.selection, customStatsPeriod = _a.customStatsPeriod;
        var data = this.state.data;
        // when there is no discover feature open events page
        var hasDiscoverQuery = organization.features.includes('discover-basic');
        var queryTerms = [];
        if (isFiltered && typeof query === 'string') {
            var queryObj = stream_1.queryToObj(query);
            for (var queryTag in queryObj)
                if (!DiscoveryExclusionFields.includes(queryTag)) {
                    var queryVal = queryObj[queryTag].includes(' ')
                        ? "\"" + queryObj[queryTag] + "\""
                        : queryObj[queryTag];
                    queryTerms.push(queryTag + ":" + queryVal);
                }
            if (queryObj.__text) {
                queryTerms.push(queryObj.__text);
            }
        }
        var commonQuery = { projects: [Number(data.project.id)] };
        var searchQuery = (queryTerms.length ? ' ' : '') + queryTerms.join(' ');
        if (hasDiscoverQuery) {
            var _b = customStatsPeriod !== null && customStatsPeriod !== void 0 ? customStatsPeriod : (selection.datetime || {}), period = _b.period, start = _b.start, end = _b.end;
            var discoverQuery = tslib_1.__assign(tslib_1.__assign({}, commonQuery), { id: undefined, name: data.title || data.type, fields: ['title', 'release', 'environment', 'user', 'timestamp'], orderby: '-timestamp', query: "issue.id:" + data.id + searchQuery, version: 2 });
            if (!!start && !!end) {
                discoverQuery.start = String(start);
                discoverQuery.end = String(end);
            }
            else {
                discoverQuery.range = period || constants_1.DEFAULT_STATS_PERIOD;
            }
            var discoverView = eventView_1.default.fromSavedQuery(discoverQuery);
            return discoverView.getResultsViewUrlTarget(organization.slug);
        }
        return {
            pathname: "/organizations/" + organization.slug + "/issues/" + data.id + "/events/",
            query: tslib_1.__assign(tslib_1.__assign({}, commonQuery), { query: searchQuery }),
        };
    };
    StreamGroup.prototype.renderReprocessingColumns = function () {
        var data = this.state.data;
        var _a = data, statusDetails = _a.statusDetails, count = _a.count;
        var info = statusDetails.info, pendingEvents = statusDetails.pendingEvents;
        var totalEvents = info.totalEvents, dateCreated = info.dateCreated;
        var remainingEventsToReprocess = totalEvents - pendingEvents;
        var remainingEventsToReprocessPercent = utils_2.percent(remainingEventsToReprocess, totalEvents);
        var value = remainingEventsToReprocessPercent || 100;
        return (<React.Fragment>
        <StartedColumn>
          <timeSince_1.default date={dateCreated}/>
        </StartedColumn>
        <EventsReprocessedColumn>
          {!utils_2.defined(count) ? (<placeholder_1.default height="17px"/>) : (<React.Fragment>
              <count_1.default value={totalEvents}/>
              {'/'}
              <count_1.default value={Number(count)}/>
            </React.Fragment>)}
        </EventsReprocessedColumn>
        <ProgressColumn>
          <progressBar_1.default value={value}/>
        </ProgressColumn>
      </React.Fragment>);
    };
    StreamGroup.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.state, data = _c.data, reviewed = _c.reviewed, actionTaken = _c.actionTaken;
        var _d = this.props, index = _d.index, query = _d.query, hasGuideAnchor = _d.hasGuideAnchor, canSelect = _d.canSelect, memberList = _d.memberList, withChart = _d.withChart, statsPeriod = _d.statsPeriod, selection = _d.selection, organization = _d.organization, displayReprocessingLayout = _d.displayReprocessingLayout, showInboxTime = _d.showInboxTime, useFilteredStats = _d.useFilteredStats, useTintRow = _d.useTintRow, customStatsPeriod = _d.customStatsPeriod, display = _d.display, queryFilterDescription = _d.queryFilterDescription, narrowGroups = _d.narrowGroups;
        var _e = selection.datetime || {}, period = _e.period, start = _e.start, end = _e.end;
        var summary = (_a = customStatsPeriod === null || customStatsPeriod === void 0 ? void 0 : customStatsPeriod.label.toLowerCase()) !== null && _a !== void 0 ? _a : (!!start && !!end
            ? 'time range'
            : utils_1.getRelativeSummary(period || constants_1.DEFAULT_STATS_PERIOD).toLowerCase());
        // Use data.filtered to decide on which value to use
        // In case of the query has filters but we avoid showing both sets of filtered/unfiltered stats
        // we use useFilteredStats param passed to Group for deciding
        var primaryCount = data.filtered ? data.filtered.count : data.count;
        var secondaryCount = data.filtered ? data.count : undefined;
        var primaryUserCount = data.filtered ? data.filtered.userCount : data.userCount;
        var secondaryUserCount = data.filtered ? data.userCount : undefined;
        var showSecondaryPoints = Boolean(withChart && data && data.filtered && statsPeriod && useFilteredStats);
        var showSessions = display === utils_3.IssueDisplayOptions.SESSIONS;
        // calculate a percentage count based on session data if the user has selected sessions display
        var primaryPercent = showSessions &&
            data.sessionCount &&
            formatters_1.formatPercentage(Number(primaryCount) / Number(data.sessionCount));
        var secondaryPercent = showSessions &&
            data.sessionCount &&
            secondaryCount &&
            formatters_1.formatPercentage(Number(secondaryCount) / Number(data.sessionCount));
        return (<Wrapper data-test-id="group" onClick={displayReprocessingLayout ? undefined : this.toggleSelect} reviewed={reviewed} unresolved={data.status === 'unresolved'} actionTaken={actionTaken} useTintRow={useTintRow !== null && useTintRow !== void 0 ? useTintRow : true}>
        {canSelect && (<GroupCheckBoxWrapper>
            <groupCheckBox_1.default id={data.id} disabled={!!displayReprocessingLayout}/>
          </GroupCheckBoxWrapper>)}
        <GroupSummary canSelect={!!canSelect}>
          <eventOrGroupHeader_1.default index={index} organization={organization} includeLink data={data} query={query} size="normal" onClick={this.trackClick}/>
          <eventOrGroupExtraDetails_1.default hasGuideAnchor={hasGuideAnchor} data={data} showInboxTime={showInboxTime}/>
        </GroupSummary>
        {hasGuideAnchor && <guideAnchor_1.default target="issue_stream"/>}
        {withChart && !displayReprocessingLayout && (<ChartWrapper className={"hidden-xs hidden-sm " + (narrowGroups ? 'hidden-md' : '')}>
            {!((_b = data.filtered) === null || _b === void 0 ? void 0 : _b.stats) && !data.stats ? (<placeholder_1.default height="24px"/>) : (<groupChart_1.default statsPeriod={statsPeriod} data={data} showSecondaryPoints={showSecondaryPoints}/>)}
          </ChartWrapper>)}
        {displayReprocessingLayout ? (this.renderReprocessingColumns()) : (<React.Fragment>
            <EventUserWrapper>
              {!utils_2.defined(primaryCount) ? (<placeholder_1.default height="18px"/>) : (<dropdownMenu_1.default isNestedDropdown>
                  {function (_a) {
                        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                        var topLevelCx = classnames_1.default('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<guideAnchor_1.default target="dynamic_counts" disabled={!hasGuideAnchor}>
                        <span {...getRootProps({
                            className: topLevelCx,
                        })}>
                          <span {...getActorProps({})}>
                            <div className="dropdown-actor-title">
                              {primaryPercent ? (<PrimaryPercent>{primaryPercent}</PrimaryPercent>) : (<PrimaryCount value={primaryCount}/>)}
                              {secondaryCount !== undefined &&
                                useFilteredStats &&
                                (secondaryPercent ? (<SecondaryPercent>{secondaryPercent}</SecondaryPercent>) : (<SecondaryCount value={secondaryCount}/>))}
                            </div>
                          </span>
                          {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                              {data.filtered && (<React.Fragment>
                                  <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                                    <MenuItemText>
                                      {queryFilterDescription !== null && queryFilterDescription !== void 0 ? queryFilterDescription : locale_1.t('Matching search filters')}
                                    </MenuItemText>
                                    {primaryPercent ? (<MenuItemPercent>{primaryPercent}</MenuItemPercent>) : (<MenuItemCount value={data.filtered.count}/>)}
                                  </StyledMenuItem>
                                  <menuItem_1.default divider/>
                                </React.Fragment>)}

                              <StyledMenuItem to={_this.getDiscoverUrl()}>
                                <MenuItemText>{locale_1.t("Total in " + summary)}</MenuItemText>
                                {secondaryPercent ? (<MenuItemPercent>{secondaryPercent}</MenuItemPercent>) : (<MenuItemCount value={secondaryPercent || data.count}/>)}
                              </StyledMenuItem>

                              {data.lifetime && (<React.Fragment>
                                  <menuItem_1.default divider/>
                                  <StyledMenuItem>
                                    <MenuItemText>{locale_1.t('Since issue began')}</MenuItemText>
                                    <MenuItemCount value={data.lifetime.count}/>
                                  </StyledMenuItem>
                                </React.Fragment>)}
                            </StyledDropdownList>)}
                        </span>
                      </guideAnchor_1.default>);
                    }}
                </dropdownMenu_1.default>)}
            </EventUserWrapper>
            <EventUserWrapper>
              {!utils_2.defined(primaryUserCount) ? (<placeholder_1.default height="18px"/>) : (<dropdownMenu_1.default isNestedDropdown>
                  {function (_a) {
                        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                        var topLevelCx = classnames_1.default('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<span {...getRootProps({
                            className: topLevelCx,
                        })}>
                        <span {...getActorProps({})}>
                          <div className="dropdown-actor-title">
                            <PrimaryCount value={primaryUserCount}/>
                            {secondaryUserCount !== undefined && useFilteredStats && (<SecondaryCount dark value={secondaryUserCount}/>)}
                          </div>
                        </span>
                        {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                            {data.filtered && (<React.Fragment>
                                <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                                  <MenuItemText>
                                    {queryFilterDescription !== null && queryFilterDescription !== void 0 ? queryFilterDescription : locale_1.t('Matching search filters')}
                                  </MenuItemText>
                                  <MenuItemCount value={data.filtered.userCount}/>
                                </StyledMenuItem>
                                <menuItem_1.default divider/>
                              </React.Fragment>)}

                            <StyledMenuItem to={_this.getDiscoverUrl()}>
                              <MenuItemText>{locale_1.t("Total in " + summary)}</MenuItemText>
                              <MenuItemCount value={data.userCount}/>
                            </StyledMenuItem>

                            {data.lifetime && (<React.Fragment>
                                <menuItem_1.default divider/>
                                <StyledMenuItem>
                                  <MenuItemText>{locale_1.t('Since issue began')}</MenuItemText>
                                  <MenuItemCount value={data.lifetime.userCount}/>
                                </StyledMenuItem>
                              </React.Fragment>)}
                          </StyledDropdownList>)}
                      </span>);
                    }}
                </dropdownMenu_1.default>)}
            </EventUserWrapper>
            <AssigneeWrapper className="hidden-xs hidden-sm">
              <assigneeSelector_1.default id={data.id} memberList={memberList} onAssign={this.trackAssign}/>
            </AssigneeWrapper>
          </React.Fragment>)}
      </Wrapper>);
    };
    StreamGroup.defaultProps = defaultProps;
    return StreamGroup;
}(React.Component));
exports.default = withGlobalSelection_1.default(withOrganization_1.default(StreamGroup));
// Position for wrapper is relative for overlay actions
var Wrapper = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  padding: ", " 0;\n  line-height: 1.1;\n\n  ", ";\n"], ["\n  position: relative;\n  padding: ", " 0;\n  line-height: 1.1;\n\n  ", ";\n"])), space_1.default(1.5), function (p) {
    return p.useTintRow &&
        (p.reviewed || !p.unresolved) &&
        !p.actionTaken && react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n      animation: tintRow 0.2s linear forwards;\n      position: relative;\n\n      /*\n       * A mask that fills the entire row and makes the text opaque. Doing this because\n       * opacity adds a stacking context in CSS so we need to apply it to another element.\n       */\n      &:after {\n        content: '';\n        pointer-events: none;\n        position: absolute;\n        left: 0;\n        right: 0;\n        top: 0;\n        bottom: 0;\n        width: 100%;\n        height: 100%;\n        background-color: ", ";\n        opacity: 0.4;\n        z-index: 1;\n      }\n\n      @keyframes tintRow {\n        0% {\n          background-color: ", ";\n        }\n        100% {\n          background-color: ", ";\n        }\n      }\n    "], ["\n      animation: tintRow 0.2s linear forwards;\n      position: relative;\n\n      /*\n       * A mask that fills the entire row and makes the text opaque. Doing this because\n       * opacity adds a stacking context in CSS so we need to apply it to another element.\n       */\n      &:after {\n        content: '';\n        pointer-events: none;\n        position: absolute;\n        left: 0;\n        right: 0;\n        top: 0;\n        bottom: 0;\n        width: 100%;\n        height: 100%;\n        background-color: ", ";\n        opacity: 0.4;\n        z-index: 1;\n      }\n\n      @keyframes tintRow {\n        0% {\n          background-color: ", ";\n        }\n        100% {\n          background-color: ", ";\n        }\n      }\n    "])), p.theme.bodyBackground, p.theme.bodyBackground, p.theme.backgroundSecondary);
});
var GroupSummary = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  margin-left: ", ";\n  margin-right: ", ";\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"], ["\n  overflow: hidden;\n  margin-left: ", ";\n  margin-right: ", ";\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"])), function (p) { return space_1.default(p.canSelect ? 1 : 2); }, space_1.default(1), function (p) { return p.theme.breakpoints[1]; });
var GroupCheckBoxWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n  align-self: flex-start;\n\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  margin-left: ", ";\n  align-self: flex-start;\n\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])), space_1.default(2));
var primaryStatStyle = function (theme) { return react_1.css(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), theme.fontSizeLarge); };
var PrimaryCount = styled_1.default(count_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return primaryStatStyle(p.theme); });
var PrimaryPercent = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return primaryStatStyle(p.theme); });
var secondaryStatStyle = function (theme) { return react_1.css(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"], ["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"])), theme.fontSizeLarge, space_1.default(0.25), theme.gray300); };
var SecondaryCount = styled_1.default(function (_a) {
    var value = _a.value, p = tslib_1.__rest(_a, ["value"]);
    return <count_1.default {...p} value={value}/>;
})(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return secondaryStatStyle(p.theme); });
var SecondaryPercent = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return secondaryStatStyle(p.theme); });
var StyledDropdownList = styled_1.default('ul')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.hovercard; });
var StyledMenuItem = styled_1.default(function (_a) {
    var to = _a.to, children = _a.children, p = tslib_1.__rest(_a, ["to", "children"]);
    return (<menuItem_1.default noAnchor>
    {to ? (
        // @ts-expect-error allow target _blank for this link to open in new window
        <link_1.default to={to} target="_blank">
        <div {...p}>{children}</div>
      </link_1.default>) : (<div className="dropdown-toggle">
        <div {...p}>{children}</div>
      </div>)}
  </menuItem_1.default>);
})(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"], ["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"])));
var menuItemStatStyles = react_1.css(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"], ["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"])), space_1.default(1));
var MenuItemCount = styled_1.default(function (_a) {
    var value = _a.value, p = tslib_1.__rest(_a, ["value"]);
    return (<div {...p}>
    <count_1.default value={value}/>
  </div>);
})(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  ", ";\n  color: ", ";\n"], ["\n  ", ";\n  color: ", ";\n"])), menuItemStatStyles, function (p) { return p.theme.subText; });
var MenuItemPercent = styled_1.default('div')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), menuItemStatStyles);
var MenuItemText = styled_1.default('div')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n  color: ", ";\n"], ["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n  color: ", ";\n"])), space_1.default(1), function (p) { return p.theme.textColor; });
var ChartWrapper = styled_1.default('div')(templateObject_17 || (templateObject_17 = tslib_1.__makeTemplateObject(["\n  width: 160px;\n  margin: 0 ", ";\n  align-self: center;\n"], ["\n  width: 160px;\n  margin: 0 ", ";\n  align-self: center;\n"])), space_1.default(2));
var EventUserWrapper = styled_1.default('div')(templateObject_18 || (templateObject_18 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[3]; });
var AssigneeWrapper = styled_1.default('div')(templateObject_19 || (templateObject_19 = tslib_1.__makeTemplateObject(["\n  width: 80px;\n  margin: 0 ", ";\n  align-self: center;\n"], ["\n  width: 80px;\n  margin: 0 ", ";\n  align-self: center;\n"])), space_1.default(2));
// Reprocessing
var StartedColumn = styled_1.default('div')(templateObject_20 || (templateObject_20 = tslib_1.__makeTemplateObject(["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 140px;\n  }\n"], ["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 140px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.gray500; }, overflowEllipsis_1.default, function (p) { return p.theme.breakpoints[0]; });
var EventsReprocessedColumn = styled_1.default('div')(templateObject_21 || (templateObject_21 = tslib_1.__makeTemplateObject(["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.gray500; }, overflowEllipsis_1.default, function (p) { return p.theme.breakpoints[0]; });
var ProgressColumn = styled_1.default('div')(templateObject_22 || (templateObject_22 = tslib_1.__makeTemplateObject(["\n  margin: 0 ", ";\n  align-self: center;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"], ["\n  margin: 0 ", ";\n  align-self: center;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19, templateObject_20, templateObject_21, templateObject_22;
//# sourceMappingURL=group.jsx.map