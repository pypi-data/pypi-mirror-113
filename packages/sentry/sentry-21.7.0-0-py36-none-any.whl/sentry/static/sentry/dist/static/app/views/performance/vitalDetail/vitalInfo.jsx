Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var vitalsCardsDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/performance/vitals/vitalsCardsDiscoverQuery"));
var vitalsCards_1 = require("../landing/vitalsCards");
function vitalInfo(props) {
    var vital = props.vital, eventView = props.eventView, organization = props.organization, location = props.location, hideBar = props.hideBar, hideStates = props.hideStates, hideVitalPercentNames = props.hideVitalPercentNames, hideDurationDetail = props.hideDurationDetail;
    return (<vitalsCardsDiscoverQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} vitals={Array.isArray(vital) ? vital : [vital]}>
      {function (_a) {
            var isLoading = _a.isLoading, vitalsData = _a.vitalsData;
            return (<vitalsCards_1.VitalBar isLoading={isLoading} data={vitalsData} vital={vital} showBar={!hideBar} showStates={!hideStates} showVitalPercentNames={!hideVitalPercentNames} showDurationDetail={!hideDurationDetail}/>);
        }}
    </vitalsCardsDiscoverQuery_1.default>);
}
exports.default = vitalInfo;
//# sourceMappingURL=vitalInfo.jsx.map