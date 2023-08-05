Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var dropdownLink_1 = tslib_1.__importDefault(require("app/components/dropdownLink"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var utils_1 = require("app/components/quickTrace/utils");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var platformCategories_1 = require("app/data/platformCategories");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var docs_1 = require("app/utils/docs");
var formatters_1 = require("app/utils/formatters");
var localStorage_1 = tslib_1.__importDefault(require("app/utils/localStorage"));
var utils_2 = require("app/utils/performance/quickTrace/utils");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var FRONTEND_PLATFORMS = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(platformCategories_1.frontend)), tslib_1.__read(platformCategories_1.mobile));
var BACKEND_PLATFORMS = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(platformCategories_1.backend)), tslib_1.__read(platformCategories_1.serverless));
var styles_1 = require("./styles");
var TOOLTIP_PREFIX = {
    root: 'root',
    ancestors: 'ancestor',
    parent: 'parent',
    current: '',
    children: 'child',
    descendants: 'descendant',
};
function QuickTrace(_a) {
    var event = _a.event, quickTrace = _a.quickTrace, location = _a.location, organization = _a.organization, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest;
    var parsedQuickTrace;
    try {
        parsedQuickTrace = utils_2.parseQuickTrace(quickTrace, event, organization);
    }
    catch (error) {
        return <React.Fragment>{'\u2014'}</React.Fragment>;
    }
    var traceLength = quickTrace.trace && quickTrace.trace.length;
    var root = parsedQuickTrace.root, ancestors = parsedQuickTrace.ancestors, parent = parsedQuickTrace.parent, children = parsedQuickTrace.children, descendants = parsedQuickTrace.descendants, current = parsedQuickTrace.current;
    var nodes = [];
    if (root) {
        nodes.push(<EventNodeSelector key="root-node" location={location} organization={organization} events={[root]} currentEvent={event} text={locale_1.t('Root')} anchor={anchor} nodeKey="root" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="root-connector"/>);
    }
    if (ancestors === null || ancestors === void 0 ? void 0 : ancestors.length) {
        nodes.push(<EventNodeSelector key="ancestors-node" location={location} organization={organization} events={ancestors} currentEvent={event} text={locale_1.tn('%s Ancestor', '%s Ancestors', ancestors.length)} anchor={anchor} nodeKey="ancestors" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="ancestors-connector"/>);
    }
    if (parent) {
        nodes.push(<EventNodeSelector key="parent-node" location={location} organization={organization} events={[parent]} currentEvent={event} text={locale_1.t('Parent')} anchor={anchor} nodeKey="parent" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<styles_1.TraceConnector key="parent-connector"/>);
    }
    var currentNode = (<EventNodeSelector key="current-node" location={location} organization={organization} text={locale_1.t('This Event')} events={[current]} currentEvent={event} anchor={anchor} nodeKey="current" errorDest={errorDest} transactionDest={transactionDest}/>);
    if (traceLength === 1) {
        nodes.push(<projects_1.default key="missing-services" orgId={organization.slug} slugs={[current.project_slug]}>
        {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === current.project_slug; });
                if (project === null || project === void 0 ? void 0 : project.platform) {
                    if (BACKEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="right"/>
                  {currentNode}
                </React.Fragment>);
                    }
                    else if (FRONTEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  {currentNode}
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="left"/>
                </React.Fragment>);
                    }
                }
                return currentNode;
            }}
      </projects_1.default>);
    }
    else {
        nodes.push(currentNode);
    }
    if (children.length) {
        nodes.push(<styles_1.TraceConnector key="children-connector"/>);
        nodes.push(<EventNodeSelector key="children-node" location={location} organization={organization} events={children} currentEvent={event} text={locale_1.tn('%s Child', '%s Children', children.length)} anchor={anchor} nodeKey="children" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    if (descendants === null || descendants === void 0 ? void 0 : descendants.length) {
        nodes.push(<styles_1.TraceConnector key="descendants-connector"/>);
        nodes.push(<EventNodeSelector key="descendants-node" location={location} organization={organization} events={descendants} currentEvent={event} text={locale_1.tn('%s Descendant', '%s Descendants', descendants.length)} anchor={anchor} nodeKey="descendants" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    return <styles_1.QuickTraceContainer>{nodes}</styles_1.QuickTraceContainer>;
}
exports.default = QuickTrace;
function handleNode(key, organization) {
    analytics_1.trackAnalyticsEvent({
        eventKey: 'quick_trace.node.clicked',
        eventName: 'Quick Trace: Node clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function handleDropdownItem(key, organization, extra) {
    analytics_1.trackAnalyticsEvent({
        eventKey: 'quick_trace.dropdown.clicked' + (extra ? '_extra' : ''),
        eventName: 'Quick Trace: Dropdown clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function EventNodeSelector(_a) {
    var location = _a.location, organization = _a.organization, _b = _a.events, events = _b === void 0 ? [] : _b, text = _a.text, currentEvent = _a.currentEvent, nodeKey = _a.nodeKey, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest, _c = _a.numEvents, numEvents = _c === void 0 ? 5 : _c;
    var errors = events.flatMap(function (event) { var _a; return (_a = event.errors) !== null && _a !== void 0 ? _a : []; });
    var type = nodeKey === 'current' ? 'black' : 'white';
    if (errors.length > 0) {
        type = nodeKey === 'current' ? 'error' : 'warning';
        text = (<styles_1.ErrorNodeContent>
        <icons_1.IconFire size="xs"/>
        {text}
      </styles_1.ErrorNodeContent>);
    }
    // make sure to exclude the current event from the dropdown
    events = events.filter(function (event) { return event.event_id !== currentEvent.id; });
    errors = errors.filter(function (error) { return error.event_id !== currentEvent.id; });
    if (events.length + errors.length === 0) {
        return <styles_1.EventNode type={type}>{text}</styles_1.EventNode>;
    }
    else if (events.length + errors.length === 1) {
        /**
         * When there is only 1 event, clicking the node should take the user directly to
         * the event without additional steps.
         */
        var hoverText = errors.length ? (locale_1.t('View the error for this Transaction')) : (<styles_1.SingleEventHoverText event={events[0]}/>);
        var target = errors.length
            ? utils_1.generateSingleErrorTarget(errors[0], organization, location, errorDest)
            : utils_1.generateSingleTransactionTarget(events[0], organization, location, transactionDest);
        return (<StyledEventNode text={text} hoverText={hoverText} to={target} onClick={function () { return handleNode(nodeKey, organization); }} type={type}/>);
    }
    else {
        /**
         * When there is more than 1 event, clicking the node should expand a dropdown to
         * allow the user to select which event to go to.
         */
        var hoverText = locale_1.tct('View [eventPrefix] [eventType]', {
            eventPrefix: TOOLTIP_PREFIX[nodeKey],
            eventType: errors.length && events.length
                ? 'events'
                : events.length
                    ? 'transactions'
                    : 'errors',
        });
        return (<styles_1.DropdownContainer>
        <dropdownLink_1.default caret={false} title={<StyledEventNode text={text} hoverText={hoverText} type={type}/>} anchorRight={anchor === 'right'}>
          {errors.length > 0 && (<styles_1.DropdownMenuHeader first>
              {locale_1.tn('Related Error', 'Related Errors', errors.length)}
            </styles_1.DropdownMenuHeader>)}
          {errors.slice(0, numEvents).map(function (error) {
                var target = utils_1.generateSingleErrorTarget(error, organization, location, errorDest);
                return (<DropdownNodeItem key={error.event_id} event={error} to={target} allowDefaultEvent onSelect={function () { return handleDropdownItem(nodeKey, organization, false); }} organization={organization} anchor={anchor}/>);
            })}
          {events.length > 0 && (<styles_1.DropdownMenuHeader first={errors.length === 0}>
              {locale_1.tn('Transaction', 'Transactions', events.length)}
            </styles_1.DropdownMenuHeader>)}
          {events.slice(0, numEvents).map(function (event) {
                var target = utils_1.generateSingleTransactionTarget(event, organization, location, transactionDest);
                return (<DropdownNodeItem key={event.event_id} event={event} to={target} onSelect={function () { return handleDropdownItem(nodeKey, organization, false); }} allowDefaultEvent organization={organization} subtext={formatters_1.getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)} anchor={anchor}/>);
            })}
          {(errors.length > numEvents || events.length > numEvents) && (<styles_1.DropdownItem to={utils_1.generateTraceTarget(currentEvent, organization)} allowDefaultEvent onSelect={function () { return handleDropdownItem(nodeKey, organization, true); }}>
              {locale_1.t('View all events')}
            </styles_1.DropdownItem>)}
        </dropdownLink_1.default>
      </styles_1.DropdownContainer>);
    }
}
function DropdownNodeItem(_a) {
    var event = _a.event, onSelect = _a.onSelect, to = _a.to, allowDefaultEvent = _a.allowDefaultEvent, organization = _a.organization, subtext = _a.subtext, anchor = _a.anchor;
    return (<styles_1.DropdownItem to={to} onSelect={onSelect} allowDefaultEvent={allowDefaultEvent}>
      <styles_1.DropdownItemSubContainer>
        <projects_1.default orgId={organization.slug} slugs={[event.project_slug]}>
          {function (_a) {
            var projects = _a.projects;
            var project = projects.find(function (p) { return p.slug === event.project_slug; });
            return (<projectBadge_1.default disableLink hideName project={project ? project : { slug: event.project_slug }} avatarSize={16}/>);
        }}
        </projects_1.default>
        {utils_1.isQuickTraceEvent(event) ? (<styles_1.StyledTruncate value={event.transaction} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={35} leftTrim trimRegex={/\.|\//g}/>) : (<styles_1.StyledTruncate value={event.title} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={45}/>)}
      </styles_1.DropdownItemSubContainer>
      {subtext && <styles_1.SectionSubtext>{subtext}</styles_1.SectionSubtext>}
    </styles_1.DropdownItem>);
}
function StyledEventNode(_a) {
    var text = _a.text, hoverText = _a.hoverText, to = _a.to, onClick = _a.onClick, _b = _a.type, type = _b === void 0 ? 'white' : _b;
    return (<tooltip_1.default position="top" containerDisplayMode="inline-flex" title={hoverText}>
      <styles_1.EventNode type={type} icon={null} to={to} onClick={onClick}>
        {text}
      </styles_1.EventNode>
    </tooltip_1.default>);
}
var HIDE_MISSING_SERVICE_KEY = 'quick-trace:hide-missing-services';
// 30 days
var HIDE_MISSING_EXPIRES = 1000 * 60 * 60 * 24 * 30;
function readHideMissingServiceState() {
    var value = localStorage_1.default.getItem(HIDE_MISSING_SERVICE_KEY);
    if (value === null) {
        return false;
    }
    var expires = parseInt(value, 10);
    var now = new Date().getTime();
    return expires > now;
}
var MissingServiceNode = /** @class */ (function (_super) {
    tslib_1.__extends(MissingServiceNode, _super);
    function MissingServiceNode() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hideMissing: readHideMissingServiceState(),
        };
        _this.dismissMissingService = function () {
            var _a = _this.props, organization = _a.organization, platform = _a.platform;
            var now = new Date().getTime();
            localStorage_1.default.setItem(HIDE_MISSING_SERVICE_KEY, (now + HIDE_MISSING_EXPIRES).toString());
            _this.setState({ hideMissing: true });
            analytics_1.trackAnalyticsEvent({
                eventKey: 'quick_trace.missing_service.dismiss',
                eventName: 'Quick Trace: Missing Service Dismissed',
                organization_id: parseInt(organization.id, 10),
                platform: platform,
            });
        };
        _this.trackExternalLink = function () {
            var _a = _this.props, organization = _a.organization, platform = _a.platform;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'quick_trace.missing_service.docs',
                eventName: 'Quick Trace: Missing Service Clicked',
                organization_id: parseInt(organization.id, 10),
                platform: platform,
            });
        };
        return _this;
    }
    MissingServiceNode.prototype.render = function () {
        var hideMissing = this.state.hideMissing;
        var _a = this.props, anchor = _a.anchor, connectorSide = _a.connectorSide, platform = _a.platform;
        if (hideMissing) {
            return null;
        }
        var docPlatform = docs_1.getDocsPlatform(platform, true);
        var docsHref = docPlatform === null || docPlatform === 'javascript'
            ? 'https://docs.sentry.io/platforms/javascript/performance/connect-services/'
            : "https://docs.sentry.io/platforms/" + docPlatform + "/performance#connecting-services";
        return (<React.Fragment>
        {connectorSide === 'left' && <styles_1.TraceConnector />}
        <styles_1.DropdownContainer>
          <dropdownLink_1.default caret={false} title={<StyledEventNode type="white" hoverText={locale_1.t('No services connected')} text="???"/>} anchorRight={anchor === 'right'}>
            <styles_1.DropdownItem width="small">
              <styles_1.ExternalDropdownLink href={docsHref} onClick={this.trackExternalLink}>
                {locale_1.t('Connect to a service')}
              </styles_1.ExternalDropdownLink>
            </styles_1.DropdownItem>
            <styles_1.DropdownItem onSelect={this.dismissMissingService} width="small">
              {locale_1.t('Dismiss')}
            </styles_1.DropdownItem>
          </dropdownLink_1.default>
        </styles_1.DropdownContainer>
        {connectorSide === 'right' && <styles_1.TraceConnector />}
      </React.Fragment>);
    };
    return MissingServiceNode;
}(React.Component));
//# sourceMappingURL=index.jsx.map