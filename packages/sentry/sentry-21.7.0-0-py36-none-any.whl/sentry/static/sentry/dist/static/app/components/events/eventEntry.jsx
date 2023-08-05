Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var breadcrumbs_1 = tslib_1.__importDefault(require("app/components/events/interfaces/breadcrumbs"));
var csp_1 = tslib_1.__importDefault(require("app/components/events/interfaces/csp"));
var debugMeta_1 = tslib_1.__importDefault(require("app/components/events/interfaces/debugMeta"));
var debugMeta_v2_1 = tslib_1.__importDefault(require("app/components/events/interfaces/debugMeta-v2"));
var exception_1 = tslib_1.__importDefault(require("app/components/events/interfaces/exception"));
var generic_1 = tslib_1.__importDefault(require("app/components/events/interfaces/generic"));
var message_1 = tslib_1.__importDefault(require("app/components/events/interfaces/message"));
var request_1 = tslib_1.__importDefault(require("app/components/events/interfaces/request"));
var spans_1 = tslib_1.__importDefault(require("app/components/events/interfaces/spans"));
var stacktrace_1 = tslib_1.__importDefault(require("app/components/events/interfaces/stacktrace"));
var template_1 = tslib_1.__importDefault(require("app/components/events/interfaces/template"));
var threads_1 = tslib_1.__importDefault(require("app/components/events/interfaces/threads"));
var event_1 = require("app/types/event");
function EventEntry(_a) {
    var _b;
    var entry = _a.entry, projectSlug = _a.projectSlug, event = _a.event, organization = _a.organization, groupId = _a.groupId;
    switch (entry.type) {
        case event_1.EntryType.EXCEPTION: {
            var data_1 = entry.data, type = entry.type;
            return <exception_1.default type={type} event={event} data={data_1} projectId={projectSlug}/>;
        }
        case event_1.EntryType.MESSAGE: {
            var data_2 = entry.data;
            return <message_1.default data={data_2}/>;
        }
        case event_1.EntryType.REQUEST: {
            var data_3 = entry.data, type = entry.type;
            return <request_1.default type={type} event={event} data={data_3}/>;
        }
        case event_1.EntryType.STACKTRACE: {
            var data_4 = entry.data, type = entry.type;
            return <stacktrace_1.default type={type} event={event} data={data_4} projectId={projectSlug}/>;
        }
        case event_1.EntryType.TEMPLATE: {
            var data_5 = entry.data, type = entry.type;
            return <template_1.default type={type} event={event} data={data_5}/>;
        }
        case event_1.EntryType.CSP: {
            var data_6 = entry.data;
            return <csp_1.default event={event} data={data_6}/>;
        }
        case event_1.EntryType.EXPECTCT:
        case event_1.EntryType.EXPECTSTAPLE:
        case event_1.EntryType.HPKP: {
            var data_7 = entry.data, type = entry.type;
            return <generic_1.default type={type} data={data_7}/>;
        }
        case event_1.EntryType.BREADCRUMBS: {
            var data_8 = entry.data, type = entry.type;
            return (<breadcrumbs_1.default type={type} data={data_8} organization={organization} event={event}/>);
        }
        case event_1.EntryType.THREADS: {
            var data_9 = entry.data, type = entry.type;
            return <threads_1.default type={type} event={event} data={data_9} projectId={projectSlug}/>;
        }
        case event_1.EntryType.DEBUGMETA:
            var data = entry.data;
            var hasImagesLoadedV2Feature = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('images-loaded-v2'));
            if (hasImagesLoadedV2Feature) {
                return (<debugMeta_v2_1.default event={event} projectId={projectSlug} groupId={groupId} organization={organization} data={data}/>);
            }
            return (<debugMeta_1.default event={event} projectId={projectSlug} organization={organization} data={data}/>);
        case event_1.EntryType.SPANS:
            return (<spans_1.default event={event} organization={organization}/>);
        default:
            // this should not happen
            /* eslint no-console:0 */
            window.console &&
                console.error &&
                console.error('Unregistered interface: ' + entry.type);
            return null;
    }
}
exports.default = EventEntry;
//# sourceMappingURL=eventEntry.jsx.map