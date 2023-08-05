Object.defineProperty(exports, "__esModule", { value: true });
exports.QuickTraceMetaBase = void 0;
var tslib_1 = require("tslib");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var quickTrace_1 = tslib_1.__importDefault(require("app/components/quickTrace"));
var utils_1 = require("app/components/quickTrace/utils");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var docs_1 = require("app/utils/docs");
var events_1 = require("app/utils/events");
var styles_1 = require("./styles");
function handleTraceLink(organization) {
    analytics_1.trackAnalyticsEvent({
        eventKey: 'quick_trace.trace_id.clicked',
        eventName: 'Quick Trace: Trace ID clicked',
        organization_id: parseInt(organization.id, 10),
        source: 'events',
    });
}
function QuickTraceMeta(_a) {
    var _b, _c, _d;
    var event = _a.event, location = _a.location, organization = _a.organization, quickTrace = _a.quickTrace, traceMeta = _a.traceMeta, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest, project = _a.project;
    var features = ['performance-view'];
    var noFeatureMessage = locale_1.t('Requires performance monitoring.');
    var docsLink = docs_1.getConfigureTracingDocsLink(project);
    var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : null;
    var traceTarget = utils_1.generateTraceTarget(event, organization);
    var body;
    var footer;
    if (!traceId || !quickTrace || quickTrace.trace === null) {
        // this platform doesn't support performance don't show anything here
        if (docsLink === null) {
            return null;
        }
        body = locale_1.t('Missing Trace');
        // need to configure tracing
        footer = <externalLink_1.default href={docsLink}>{locale_1.t('Read the docs')}</externalLink_1.default>;
    }
    else {
        if (quickTrace.isLoading) {
            body = <placeholder_1.default height="24px"/>;
        }
        else if (quickTrace.error) {
            body = '\u2014';
        }
        else {
            body = (<errorBoundary_1.default mini>
          <quickTrace_1.default event={event} quickTrace={{
                    type: quickTrace.type,
                    trace: quickTrace.trace,
                }} location={location} organization={organization} anchor={anchor} errorDest={errorDest} transactionDest={transactionDest}/>
        </errorBoundary_1.default>);
        }
        footer = (<link_1.default to={traceTarget} onClick={function () { return handleTraceLink(organization); }}>
        {locale_1.tct('View Full Trace: [id][events]', {
                id: events_1.getShortEventId(traceId !== null && traceId !== void 0 ? traceId : ''),
                events: traceMeta
                    ? locale_1.tn(' (%s event)', ' (%s events)', traceMeta.transactions + traceMeta.errors)
                    : '',
            })}
      </link_1.default>);
    }
    return (<feature_1.default hookName="feature-disabled:performance-quick-trace" features={features}>
      {function (_a) {
            var hasFeature = _a.hasFeature;
            // also need to enable the performance feature
            if (!hasFeature) {
                footer = (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
              {footer}
            </hovercard_1.default>);
            }
            return <QuickTraceMetaBase body={body} footer={footer}/>;
        }}
    </feature_1.default>);
}
exports.default = QuickTraceMeta;
function QuickTraceMetaBase(_a) {
    var body = _a.body, footer = _a.footer;
    return (<styles_1.MetaData headingText={locale_1.t('Trace Navigator')} tooltipText={locale_1.t('An abbreviated version of the full trace. Related frontend and backend services can be added to provide further visibility.')} bodyText={<div data-test-id="quick-trace-body">{body}</div>} subtext={<div data-test-id="quick-trace-footer">{footer}</div>}/>);
}
exports.QuickTraceMetaBase = QuickTraceMetaBase;
//# sourceMappingURL=quickTraceMeta.jsx.map