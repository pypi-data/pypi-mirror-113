Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var contextBlock_1 = tslib_1.__importDefault(require("app/components/events/contexts/contextBlock"));
function getKnownData(data) {
    return Object.entries(data)
        .filter(function (_a) {
        var _b = tslib_1.__read(_a, 1), k = _b[0];
        return k !== 'type' && k !== 'title';
    })
        .map(function (_a) {
        var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
        return ({
            key: key,
            subject: startCase_1.default(key),
            value: value,
        });
    });
}
var DefaultContextType = function (_a) {
    var data = _a.data;
    return <contextBlock_1.default data={getKnownData(data)}/>;
};
exports.default = DefaultContextType;
//# sourceMappingURL=default.jsx.map