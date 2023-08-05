Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
// TODO(Priscila): Remove BR tags
// mapUrl not always present; e.g. uploaded source maps
var OriginalSourceInfo = function (_a) {
    var mapUrl = _a.mapUrl, map = _a.map;
    if (!utils_1.defined(map) && !utils_1.defined(mapUrl)) {
        return null;
    }
    return (<react_1.Fragment>
      <strong>{locale_1.t('Source Map')}</strong>
      <br />
      {mapUrl !== null && mapUrl !== void 0 ? mapUrl : map}
      <br />
    </react_1.Fragment>);
};
exports.default = OriginalSourceInfo;
//# sourceMappingURL=originalSourceInfo.jsx.map