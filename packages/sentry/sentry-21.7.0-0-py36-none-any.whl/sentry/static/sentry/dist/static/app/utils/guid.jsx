Object.defineProperty(exports, "__esModule", { value: true });
exports.uniqueId = void 0;
function uniqueId() {
    var s4 = function () {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    };
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}
exports.uniqueId = uniqueId;
//# sourceMappingURL=guid.jsx.map