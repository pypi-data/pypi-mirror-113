Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var moment_timezone_1 = tslib_1.__importDefault(require("moment-timezone"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var utils_1 = require("app/components/events/interfaces/spans/utils");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var locale_1 = require("app/locale");
var discoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/discoverQuery"));
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var list_1 = tslib_1.__importDefault(require("./list"));
var Body = function (_a) {
    var traceID = _a.traceID, organization = _a.organization, event = _a.event, location = _a.location;
    if (!traceID) {
        return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default small withIcon={false}>
            {locale_1.t('This event has no trace context, therefore it was not possible to fetch similar issues by trace ID.')}
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
    }
    var orgSlug = organization.slug;
    var orgFeatures = organization.features;
    var dateCreated = moment_timezone_1.default(event.dateCreated).valueOf() / 1000;
    var _b = utils_1.getTraceDateTimeRange({ start: dateCreated, end: dateCreated }), start = _b.start, end = _b.end;
    var eventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        name: "Issues with Trace ID " + traceID,
        fields: ['issue.id'],
        orderby: '-timestamp',
        query: "trace:" + traceID + " !event.type:transaction !id:" + event.id + " ",
        projects: orgFeatures.includes('global-views')
            ? [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            : [Number(event.projectID)],
        version: 2,
        start: start,
        end: end,
    });
    return (<discoverQuery_1.default eventView={eventView} location={location} orgSlug={orgSlug} limit={5}>
      {function (data) {
            var _a;
            if (data.isLoading) {
                return <loadingIndicator_1.default />;
            }
            var issues = ((_a = data === null || data === void 0 ? void 0 : data.tableData) === null || _a === void 0 ? void 0 : _a.data) || [];
            return (<list_1.default issues={issues} pageLinks={data.pageLinks} traceID={traceID} orgSlug={orgSlug} location={location} period={{ start: start, end: end }}/>);
        }}
    </discoverQuery_1.default>);
};
exports.default = Body;
//# sourceMappingURL=body.jsx.map