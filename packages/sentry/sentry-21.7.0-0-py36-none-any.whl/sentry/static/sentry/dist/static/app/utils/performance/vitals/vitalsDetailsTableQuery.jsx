Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var genericDiscoverQuery_1 = tslib_1.__importDefault(require("app/utils/discover/genericDiscoverQuery"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
function VitalsCardsDiscoverQuery(props) {
    return <genericDiscoverQuery_1.default route="eventsv2" {...props}/>;
}
exports.default = withApi_1.default(VitalsCardsDiscoverQuery);
//# sourceMappingURL=vitalsDetailsTableQuery.jsx.map