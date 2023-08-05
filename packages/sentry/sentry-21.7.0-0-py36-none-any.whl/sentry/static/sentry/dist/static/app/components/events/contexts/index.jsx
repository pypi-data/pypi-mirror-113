Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var utils_1 = require("app/utils");
var chunk_1 = tslib_1.__importDefault(require("./chunk"));
function Contexts(_a) {
    var event = _a.event, group = _a.group;
    var user = event.user, contexts = event.contexts;
    return (<react_1.Fragment>
      {!utils_1.objectIsEmpty(user) && (<chunk_1.default key="user" type="user" alias="user" group={group} event={event} value={user}/>)}
      {Object.entries(contexts).map(function (_a) {
            var _b;
            var _c = tslib_1.__read(_a, 2), key = _c[0], value = _c[1];
            return (<chunk_1.default key={key} type={(_b = value === null || value === void 0 ? void 0 : value.type) !== null && _b !== void 0 ? _b : ''} alias={key} group={group} event={event} value={value}/>);
        })}
    </react_1.Fragment>);
}
exports.default = Contexts;
//# sourceMappingURL=index.jsx.map